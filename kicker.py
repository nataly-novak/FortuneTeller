import random


def kick():
    k = open('Hits','r')
    k1 = k.readlines()[:-1]
    n = len(k1)
    r = random.randrange(n)
    return k1[r]

print(kick())