alfabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,- '


def encode(text, key):
    text = text.rstrip()
    res = ''
    leng = len(alfabet)
    tl = len(text)
    kl = len(key)
    for i in range(tl):
        a = alfabet.find(text[i])+1
        b = alfabet.find(key[i % kl])+1
        c = (a + b - 1) % leng
        print(a, b, c)
        letter = alfabet[c]
        res += letter
    return res

def decode(text, key):
    text = text.rstrip()
    res = ''
    leng = len(alfabet)
    tl = len(text)
    kl = len(key)
    for i in range(tl):
        a = alfabet.find(text[i]) + 1
        b = alfabet.find(key[i % kl]) + 1
        c = (a - b - 1) % leng
        letter = alfabet[c]
        res += letter
    return res


#f = open("/home/study/Harrow", "r")
#f1 = f.readlines()
#w = open('thedeck',"w+")
#for i in f1:
#    w.write(encode(i,'PHARASMA'))
#    w.write("\n")
f = open("thedeck", "r")
f1 = f.readlines()
for i in f1:
    print(decode(i,"PHARASMA"))
