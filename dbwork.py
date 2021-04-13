import os
import psycopg2
import random
from dotenv import load_dotenv


def getconn():
    load_dotenv()

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')


    return conn







def makedb():
    conn = getconn()
    cur = conn.cursor()

    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('quotes',))
    check = (cur.fetchone()[0])
    print(check)
    if not check:
        cur.execute('''CREATE TABLE quotes (
        NUM INT  NOT NULL,
        QUOT CHAR(200)  NOT NULL
        );''')
        print("Table created successfully")
        cur.execute("ALTER TABLE quotes ADD CONSTRAINT test_pkey PRIMARY KEY (QUOT);")
    else:
        print('No need')
    conn.commit()

    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('inter',))
    check = (cur.fetchone()[0])
    if not check:
        cur.execute('''CREATE TABLE inter (
        NUM INT  NOT NULL,
        LANG CHAR (30) NOT NULL,
        QUOT CHAR(200)  NOT NULL,
        TRAN CHAR(200)
        );''')
        print("Table created successfully")
        cur.execute('ALTER TABLE inter ADD CONSTRAINT test_pkey1 PRIMARY KEY (QUOT);')
    else:
        print('No need')
    conn.commit()
    cur.close()
    conn.close()

def filldb():
    conn = getconn()
    cur = conn.cursor()
    f = open("quotes.txt", "r")
    f1 = f.readlines()
    cnt = 0
    for i in f1:
        cur.execute("INSERT INTO quotes VALUES (%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (cnt, i[:-1]))
        cnt += 1
        print(cnt)
    cur.execute("SELECT NUM, QUOT from quotes")
    rows = cur.fetchall()
    for j in rows:
        print(j)

    f = open("international", "r",encoding="utf8")
    f1 = f.readlines()
    cnt = 0
    for i in f1:
        a = i[:-1].split(' - ')
        if len(a) < 3:
            a.append('')
        cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (cnt, a[0], a[1], a[2]))
        cnt += 1
    cur.execute("SELECT NUM, LANG, QUOT, TRAN from inter")
    rows = cur.fetchall()
    n = len(f1)
    f.close()
    cur.close()
    conn.close()


def randomru():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM quotes;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    print(rr)
    cur.execute("SELECT QUOT FROM quotes WHERE NUM = %s", ([random.randrange(rr + 1)]))
    resp = str(cur.fetchone())
    response = resp[2:-3].strip()
    cur.close()
    conn.close()
    return response



def randomquote():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    dd = random.randrange(rr + 1)
    cur.execute("SELECT QUOT FROM inter WHERE NUM = %s", ([dd]))
    resp = str(cur.fetchone())
    response = resp[2:-3].strip()
    cur.execute("SELECT TRAN FROM inter WHERE NUM = %s", ([dd]))
    resp1 = str(cur.fetchone())
    response = response + ' - ' + resp1[2:-3].strip()
    cur.execute("SELECT LANG FROM inter WHERE NUM = %s", ([dd]))
    resp2 = str(cur.fetchone())
    response = response + ' - ' + resp2[2:-3].strip()
    cur.close()
    conn.close()
    return response

def addru(line):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM quotes;")
    a = str(cur.fetchone())
    if a == 'None':
        ar = 1
    else:
        ar = int(a[1:-2]) + 1
    print(ar)
    cur.execute("INSERT INTO quotes VALUES (%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (ar, line))
    conn.commit()
    cur.execute("SELECT NUM, QUOT from quotes")
    rows = cur.fetchall()
    for j in rows:
        print(j)
    cur.close()
    conn.close()

def addquote(language, line, trans=""):
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = str(cur.fetchone())
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;", (ar, language, line, trans))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x+=1
    cur.close()
    conn.close()
    return "we have "+str(x) +" quotes so far"

def removelast():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = int(str(cur.fetchone())[1:-2])
    cur.execute("DELETE FROM inter WHERE NUM = %s;", ([a]))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x+=1
    cur.close()
    conn.close()
    return "we have " + str(x) + " quotes so far"

def quotenum():
    conn = getconn()
    cur = conn.cursor()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    x = 0
    for j in rows:
        x += 1
    cur.close()
    conn.close()
    return "we have " + str(x) + " quotes so far"














