import random

def rdten():
    return random.randrange(10)+1

def roll(n):
    rolls = []
    for i in range(n):
        rolls.append(rdten())
    return rolls

def dif(n, val):

    if n > 0:
        res = roll(n)
        num = 0
        for i in res:
            if i >= val and i > num:
                num = i
        if num == 0:
            score = 0
        elif num ==10:
            score = 2
        else:
            score = 1
    else:
        m = 2-n
        res = roll(m)
        num = min(res)
        if num >= val:
            if num == 10:
                score = 2
            else:
                score = 1
        else:
            score = 0
    return([num, res, score])

def opp(n,m):
    r1 = roll(n)
    r2 = roll(m)
    m1 = 0
    m2 = 0
    for i in r1:
        if i > m1:
            m1 = i
    for i in r2:
        if i > m2:
            m2 = i
    if m1 > m2:
        res = 1
    elif m2 > m1:
        res = 2
    else:
        res = 0
    if max(m1,m2) == 10:
        tot = 1
    else:
        tot = 0
    return([r1,r2, max(m1,m2),res, tot])

def damage(n, val):
    x = dif(n,val)
    if x[2] ==0:
        wound = 0
    elif x[2] == 1:
        wound = 1
    else:
        wound = 1
        for i in x[1]:
            if i == 10:
                wound +=1
    return([x[1],wound, x[2]])

def open(n, val):
    x = dif(n,val)
    if x[2] ==0:
        wound = 0
    elif x[2] == 1:
        wound = 0
        for i in x[1]:
            if i >= val:
                wound+=1
    else:
        wound = 1
        for i in x[1]:
            if i >= val:
                wound += 1
    return ([x[1], wound, x[2]])


def parser(line):
    if '%' in line:
        x = line.split("%")
        y = x[0].split('>')
        y[0] = y[0][:-1]
        if x[1] == "d":
            res =  damage(int(y[0]),int(y[1]))
            n = 3
        else:
            res = open(int(y[0]),int(y[1]))
            n = 4
    else:
        x = line.split('>')
        print(x)
        if 'd' in x[1]:
            a = x[0][:-1]
            b = x[1][:-1]
            res =  opp(int(a),int(b))
            n = 2
        else:
            a = x[0][:-1]
            b = x[1]
            print(a,b)
            res = dif(int(a),int(b))
            n = 1
    return [n,res]

def printer(lst):
    answer = ""
    if lst[0] == 1:
        answer +=("Result: "+str(lst[1][0])+'\n')
        for i in lst[1][1]:
            answer+=(str(i)+" ")
        answer +="\n"
        if lst[1][2] ==0:
            answer+="FAIL"
        elif lst[1][2] ==1:
            answer+="SUCCESS"
        else:
            answer+="TOTAL SUCCESS"
    elif lst[0]==2:
        answer += ("Result: " + str(lst[1][2]) + '\n')
        for i in lst[1][0]:
            answer+=(str(i)+" ")
        answer +="\n"
        for i in lst[1][1]:
            answer+=(str(i)+" ")
        answer +="\n"
        if lst[1][3] == 1:
            answer += "FIRST WINS"
        elif lst[1][3] == 2:
            answer += "SECOND WINS"
        else:
            answer += "DRAW"
        if lst[1][4] == 1:
            answer +=" - TOTAL SUCCESS"
    elif lst[0] == 3:
        if lst[1][1] > 1:
            answer += (str(lst[1][1]) + " Wounds\n")
        else:
            answer += (str(lst[1][1]) + " Wound\n")
        for i in lst[1][0]:
            answer+=(str(i)+" ")
        answer +="\n"
        if lst[1][2] == 0:
            answer += "FAIL"
        elif lst[1][2] == 1:
            answer += "SUCCESS"
        else:
            answer += "TOTAL SUCCESS"
    elif lst[0] == 4:
        if lst[1][1] > 1:
            answer +=(str(lst[1][1])+" Wounds of open damage\n")
        else:
            answer += (str(lst[1][1]) + " Wound of open damage\n")
        for i in lst[1][0]:
            answer+=(str(i)+" ")
        answer +="\n"
        if lst[1][2] == 0:
            answer += "FAIL"
        elif lst[1][2] == 1:
            answer += "SUCCESS"
        else:
            answer += "TOTAL SUCCESS"
    return answer


def rbroll(line):
    return printer(parser(line))

print(rbroll("4d>6%d"))