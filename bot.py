import os
import random

from discord.ext import commands
from dotenv import load_dotenv

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


cur = conn.cursor()
#cur.execute("DROP TABLE inter")


print('koai')

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('inter',))
check = (cur.fetchone()[0])
print(check)
if not check:
    cur.execute('''CREATE TABLE inter (
    NUM INT  NOT NULL,
    LANG CHAR (30) NOT NULL,
    QUOT CHAR(200)  NOT NULL,
    TRAN CHAR(200)
    );''')
    print("Table created successfully")
    cur.execute("ALTER TABLE inter ADD CONSTRAINT test_pkey1 PRIMARY KEY (QUOT);")
else:
    print('No need')
conn.commit()

load_dotenv()

f = open("international", "r")
f1 = f.readlines()
cnt = 0
for i in f1:
    a = i[:-1].split(' - ')
    if len(a)<3:
        a.append('')
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;",(cnt,a[0],a[1],a[2]))
    cnt += 1
    print(cnt)
cur.execute("SELECT NUM, LANG, QUOT, TRAN from inter")
rows = cur.fetchall()
for j in rows:
    print(j)

n = len(f1)
print(n)
f.close()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')


@bot.command(name='quote', help = "generates random quotes with translation")
async def cookin(ctx):
    cur.execute("SELECT MAX(NUM) FROM inter;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    print(rr)
    dd = random.randrange(rr+1)
    cur.execute("SELECT QUOT FROM inter WHERE NUM = %s",([dd]))
    resp = str(cur.fetchone())
    response = resp[2:-3].strip()
    cur.execute("SELECT TRAN FROM inter WHERE NUM = %s", ([dd]))
    resp1 = str(cur.fetchone())
    response = response+' - ' +resp1[2:-3].strip()
    cur.execute("SELECT LANG FROM inter WHERE NUM = %s", ([dd]))
    resp2 = str(cur.fetchone())
    response = response+' - ' +resp2[2:-3].strip()
    print(response)
    await ctx.send(response)


@bot.command(name='add' , help='Adds a quote. Use quotes around both quote and translation')
async def itl(ctx,language, line, trans =""):
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = str(cur.fetchone())
    print(a)
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    print(ar)
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;",(ar,language,line,trans))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)


@bot.command(name='del' , help='deletes last quote')
async def de(ctx):
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = int(str(cur.fetchone())[1:-2])
    print(a)
    cur.execute("DELETE FROM inter WHERE NUM = %s;",([a]))
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)




bot.run(TOKEN)