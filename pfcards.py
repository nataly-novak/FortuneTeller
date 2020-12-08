from coder import decode
import random
import copy

coloring = {'S': "Strength", "D": "Dexterity", "C": "Constitution", "I": "Intelligence", "W": "Wisdom", "A": "Charisma"}
alignements = [['L', 'G'], ['N', 'G'], ['C', 'G'], ['L', 'N'], ['N', 'N'], ['C', 'N'], ['L', 'E'], ['N', 'E'], ['C', 'E']]
phases = ["Positive past:", "Unclear past:", "Negative past:", "Positive Present:", "Unclear Present:",
          "Negative Present:", "Positive Future:", "Unclear Future:", "Negative Future:"]
import os

CODE_KEY = 'PHARASMA'


def isOpposed(a, b):
    if (a[0] == 'L' and b[0] == 'C') or (a[0] == 'C' and b[0] == 'L') or (a[0] == 'N' and b[0] == 'N'):
        if (a[1] == 'G' and b[1] == 'E') or (a[1] == 'E' and b[1] == 'G') or (a[1] == 'N' and b[1] == 'N'):
            if (a[1] == 'N' and b[1] == 'N') and (a[0] == 'N' and b[0] == 'N'):
                return False
            else:
                return True
        else:
            return False
    else:
        return False


def isSame(a, b):
    if (a[0] == b[0]) and (a[1] == b[1]):
        return True
    else:
        return False


def isPartial(a, b):
    if (a[0] == b[0]) ^ (a[1] == b[1]):
        return True
    else:
        return False


def deckFormat():
    f = open('thedeck', 'r')
    f1 = f.readlines()
    thedeck = []
    for i in f1:
        if i != '\n':
            line = decode(i, CODE_KEY)
            x = line.split(' - ', 2)
            y = x[0].split(' ')
            r = []
            for j in y:
                r.append(j)
            r.append(x[1])
            r.append(x[2])
            thedeck.append(r)
    return thedeck


def choosing(stat, deck, num):
    color = []
    for i in range(len(deck)):
        if deck[i][0] == stat:
            color.append(i)
    draw = []
    for j in range(num):
        draw.append(color.pop(random.randrange(len(color))))
    return draw


def printDCard(n, deck):
    card = deck[n]
    res = card[3] + ' - ' + coloring[card[0]] + ": " + card[1] + card[2] + ' - ' + card[4]
    return res


def printName(n, deck):
    card = deck[n]
    res = card[3]
    return res


def spread(roles, deck):
    draw = []
    newdeck = list(range(54))
    for j in range(9):
        draw.append(newdeck.pop(random.randrange(9)))
    telling = []
    print(len(draw),len(alignements))
    for q in draw:
        card = ['', '', '']
        one = deck[q]
        a = [one[1], one[2]]
        b = alignements[draw.index(q)]
        if isSame(a, b):
            card[0] += "True Match, "
        elif isOpposed(a, b):
            card[0] += "Opposite Match, "
        elif isPartial(a, b):
            card[0] += "Partial Match, "
        if q in roles:
            card[1] += "Role " + str(roles.index(q)+1) + ","
        card[2] += printDCard(q, deck)
        telling.append(card)
    return telling


def fortuneTelling(stat, n, deck):
    roles = choosing(stat, deck, n)
    vision = spread(roles, deck)
    timeline = [vision[0], vision[3], vision[6], vision[1], vision[4], vision[7], vision[2], vision[5], vision[8]]
    l1 = ''
    for r in roles:
        l1 += printName(r, deck)+', '
    l1 = l1[:-2]
    answer = [l1]
    for t in timeline:
        line = phases[timeline.index(t)]+' '
        for f in t:
            line += f
        answer.append(line)
    return answer


