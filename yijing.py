import dice

def get_articles():
    c = open("YIJing.txt", "r")
    c1 = c.read()
    articles = c1.split("_")
    processed = []
    for i in articles:
        art = []
        i = i.strip()
        i = i.rstrip()
        art = i.split("\n")
        processed.append(art)

    return processed[1:-1]

def draw():
    res = ""
    for i in range(6):
        rolled = str(dice.roll(2)-1)
        res += rolled
    return res

def print_article(article):
    st = []
    ln = ""
    for i in article:
        if len(ln)+len(i)+10<2000:
            ln = ln+ i + "\n"
        else:
            st.append(ln)
            ln = i + "\n"
    st.append(ln)
    return st

def get_result():
    res = draw()
    print(res)
    processed = get_articles()
    for i in processed:
        if i[1]==res:
            return print_article(i)
