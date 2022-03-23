import random

def parse (line):
    buffer = ""
    adder = 0
    parsed = []
    for i in line:
        if i not in["+","-"]:
            if adder==0:
                buffer += i
            else:
                parsed.append(buffer)
                buffer = i
                adder = 0
        else:
            parsed.append(buffer)
            buffer = i
            adder = 1
    parsed.append(buffer)
    return parsed

def roll(dice):
    return random.randrange(dice) + 1

def mult(line):
    rolls = []
    parts = line.split("d")
    if parts[0] == "":
        parts[0] = 1
    for i in range(int(parts[0])):
        rolls.append(roll(int(parts[1])))
    return rolls

def keephigher(line):
    parts = line.split("kh")
    if parts[1] == "":
        parts[1] = "1"
    rolls = mult(parts[0])
    sortedrolls = sorted(rolls, reverse=True)
    num = int(parts[1])
    resultrolls = sortedrolls[:num]
    return [rolls, resultrolls]

def keeplower(line):
    parts = line.split("kl")
    if parts[1] == "":
        parts[1] = "1"
    rolls = mult(parts[0])
    sortedrolls = sorted(rolls, reverse=False)
    num = int(parts[1])
    resultrolls = sortedrolls[:num]
    return [rolls, resultrolls]

def more(roll, target):
    rolls = mult(roll)
    resultrolls = []
    tg = int(target)
    for i in rolls:
        if i >= tg:
            resultrolls.append(i)
    return [rolls, resultrolls]

def less(roll, target):
    rolls = mult(roll)
    resultrolls = []
    tg = int(target)
    for i in rolls:
        if i <= tg:
            resultrolls.append(i)
    return [rolls, resultrolls]

def explode(lst):
    full = lst[0]
    n = lst[1]
    die = lst[2]
    rolls = []
    for i in range(n):
        d = roll(die)
        full.append(d)
        rolls.append(d)
    new_n = 0
    full.append("|")
    for i in rolls:
        if i == die:
            new_n += 1
    n_lst = [full, new_n, die]
    if new_n > 0:
        return explode(n_lst)

    else:
        return n_lst


def explode_lim(lst):
    full = lst[0]
    n = lst[1]
    die = lst[2]
    lim = lst[3]
    it = lst[4]
    rolls = []
    for i in range(n):
        d = roll(die)
        full.append(d)
        rolls.append(d)
    full.append("|")
    new_n = 0
    for i in rolls:
        if i == die:
            new_n += 1
    it += 1
    n_lst = [full, new_n, die, lim, it]

    if new_n > 0 and it <= lim:
        return explode(n_lst)

    else:
        return n_lst

def explosion(line):
    parts = line.split("!")
    if parts[1] == "":
        rolls = mult(parts[0])
        die = int(parts[0].split('d')[1])
        k = 0
        for i in rolls:
            if i == die:
                k+=1
        rolls.append("|")
        lst = [rolls, k, die]
        res = (explode(lst))
        work = []
        for i in res[0]:
            if i != "|":
                work.append(i)
        return [res[0], work]
    else:
        rolls = mult(parts[0])
        die = int(parts[0].split('d')[1])
        k = 0
        for i in rolls:
            if i == die:
                k += 1
        rolls.append("|")
        lst = [rolls, k, die, int(parts[1]), 1]
        res = (explode_lim(lst))
        work = []
        for i in res[0]:
            if i != "|":
                work.append(i)
        return [res[0], work]

def wod(line):
    line = line.rstrip("w")
    parts = line.split(">")
    rolls = more(parts[0],parts[1])
    num = len(rolls[1])
    die = int(parts[0].split("d")[1])
    for i in rolls[0]:
        if i == die:
            num+=1
        elif i == 1:
            num -=1
    return [rolls[0], rolls[1], num, die]


def process(line):
    if line in ["+", "-"]:
        return [line, line, ""]
    else:
        if "d" not in line:
            return [line, int(line)]
        else:
            if ">" not in line and "<" not in line:
                if "k" not in line and "!" not in line:
                    rolls = mult(line)
                    text = "("
                    sum = 0
                    for i in rolls:
                        text = text + str(i) +", "
                        sum+=i
                    text = text.rstrip(" ,")
                    text = text +")"
                    return [text, sum]
                else:
                    if "!" in line:
                        rolls = explosion(line)
                        text = "("
                        for i in rolls[0]:
                            if i != "|":
                                text = text + str(i) + ", "
                            else:
                                text = text.rstrip(" ,")
                                text = text + ' | '
                        text = text.rstrip("| ,")
                        text = text + ")"
                        sum = 0
                        for i in rolls[1]:
                            sum += int(i)
                        return [text, sum]
                    elif "k" in line:
                        if "l" in line:
                            rolls = keeplower(line)
                        elif "h" in line:
                            rolls = keephigher(line)
                        text = "("
                        cnt = 0
                        max = len(rolls[1])
                        for i in rolls[0]:
                            if i in rolls[1] and cnt < max:
                                text = text + str(i) + ", "
                                cnt+=1
                            else:
                                text = text + "~~"+str(i) + "~~, "
                        text = text.rstrip(" ,")
                        text = text + ")"
                        sum = 0
                        for i in rolls[1]:
                            sum+=i
                        return [text, sum]
            else:
                if ">" in line:
                    if "w" in line:
                        rolls = wod(line)
                        text = "("
                        for i in rolls[0]:
                            if i in rolls[1]:
                                if i != rolls[3]:
                                    text = text + str(i)+ ", "
                                else:
                                    text = text + "**" + str(i) + "**, "
                            else:
                                if i != 1:
                                    text = text+ "~~" + str(i) + "~~, "
                                else:
                                    text = text+ "~~**" + str(i) + "**~~, "
                        text = text.rstrip(", ")+")"
                        return (text, rolls[2])
                    else:
                        parts = line.split('>')
                        rolls = more(parts[0],parts[1])
                        text = "("
                        for i in rolls[0]:
                            if i in rolls[1]:
                                text = text + str(i) + ", "
                            else:
                                text = text + "~~" + str(i) + "~~, "
                        text = text.rstrip(", ") + ")"
                        num = len(rolls[1])
                        return [text, num]
                else:
                    parts = line.split('<')
                    rolls = less(parts[0], parts[1])
                    text = "("
                    for i in rolls[0]:
                        if i in rolls[1]:
                            text = text + str(i) + ", "
                        else:
                            text = text + "~~" + str(i) + "~~, "
                    text = text.rstrip(", ") + ")"
                    num = len(rolls[1])
                    return [text, num]

def solve(line):
    fulltext = line + " ="

    num = 0
    switch = 1
    lst = parse(line)
    for i in lst:
        vals = process(i)

        if vals[1] == "+":
            switch = 1
            fulltext = fulltext + " + "
        elif vals[1] == "-":
            switch = -1
            fulltext = fulltext + " - "
        else:
            num += vals[1]*switch
            switch = 0
            fulltext += vals[0]
    fulltext = fulltext + " = "+str(num)
    return fulltext

























