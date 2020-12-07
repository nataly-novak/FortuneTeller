import random

def getCards():
    t = open("Tarot_Deck.txt", "r")
    t1 = t.readlines()
    cards = []
    n = 0
    for i in t1:
        x = i[:-1].split(' - ', 1)
        card = [n]
        card.append(x[0])
        card.append(x[1])
        n += 1
        cards.append(card)
    return cards


def getMajors():
    t = open("Tarot_Deck.txt", "r")
    t1 = t.readlines()
    cards = []
    n = 0
    for i in t1:
        x = i[:-1].split(' - ', 1)
        if n < 22:
            card = [n]
            card.append(x[0])
            card.append(x[1])
            n += 1
            cards.append(card)
    return cards


def threeMajors():
    majors = list(range(0, 78))
    draw = []
    for i in range(3):
        x =[]
        #draw.append[(majors.pop(random.randrange(len(majors)))), random.randrange(1)]
        x.append(majors.pop(random.randrange(len(majors))))
        x.append(random.randrange(2))
        draw.append(x)
    return draw

def threeCards():
    full = list(range(0, 78))
    draw = []
    for i in range(3):
        x =[]
        #draw.append[(majors.pop(random.randrange(len(majors)))), random.randrange(1)]
        x.append(full.pop(random.randrange(len(majors))))
        x.append(random.randrange(2))
        draw.append(x)
    return draw


def printCard(j):
    deck = getCards()
    card = []
    for k in range(len(deck)):
        if deck[k][0] == j[0]:
            card.append(deck[k][1])
            if j[1] == 0:
                card.append('Normal')
            else:
                card.append('Reversed')

            card.append(deck[k][2])
    return card





