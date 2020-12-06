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
    majors = list(range(0, 22))
    draw = []
    for i in range(3):
        draw.append(majors.pop(random.randrange(len(majors))))
    return draw


def printCard(j):
    deck = getCards()
    card = []
    for k in range(len(deck)):
        if deck[k][0] == j:
            card.append(deck[k][1])
            card.append(deck[k][2])
    return card





