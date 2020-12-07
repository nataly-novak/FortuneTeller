import os
import random
from tarot import threeMajors, getMajors, getCards, printCard

from discord.ext import commands
from dotenv import load_dotenv

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


cur = conn.cursor()
#cur.execute("DROP TABLE quotes")
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
load_dotenv()
f = open("quotes.txt", "r")
f1 = f.readlines()
cnt = 0
for i in f1:
    cur.execute("INSERT INTO quotes VALUES (%s,%s) ON CONFLICT (QUOT) DO NOTHING ;",(cnt,i[:-1]))
    cnt += 1
    print(cnt)
cur.execute("SELECT NUM, QUOT from quotes")
rows = cur.fetchall()
for j in rows:
    print(j)

n = len(f1)
print(n)
f.close()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='c', help = "generates random quotes")
async def cook(ctx):
    cur.execute("SELECT MAX(NUM) FROM quotes;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    print(rr)
    print(len(f1))
    cur.execute("SELECT QUOT FROM quotes WHERE NUM = %s",([random.randrange(rr+1)]))
    resp = str(cur.fetchone())
    response = resp[2:-3].strip()
    print(response)
    await ctx.send(response)

@bot.command(name='w' , help='Adds a quote. Use quotes around')
async def writ(ctx, line):
    cur.execute("SELECT MAX(NUM) FROM quotes;")
    a = str(cur.fetchone())
    ar = int(a[1:-2])+1
    print(ar)
    cur.execute("INSERT INTO quotes VALUES (%s,%s) ON CONFLICT (QUOT) DO NOTHING ;",(ar,line))
    conn.commit()
    cur.execute("SELECT NUM, QUOT from quotes")
    rows = cur.fetchall()
    for j in rows:
        print(j)

@bot.command(name='tarot' , help='')
async def tarot(ctx, variant):
    if variant == '3m':
        a = threeMajors()
        res =[]
        first =[]
        for q in a:
            x = printCard(q)
            first.append(x[0])
            res.append(x)
        s1 =(first[0]+', '+first[1]+', '+first[2])
        await ctx.send(s1)
        for u in res:
            s2 = (u[0]+' - '+u[1]+': '+u[2])
            await ctx.send(s2)



bot.run(TOKEN)