import os
import random
from tarot import threeMajors, getMajors, getCards, printCard, threeCards
from pfcards import deckFormat, fortuneTelling
from rbrb import rbroll

from discord.ext import commands
from dotenv import load_dotenv
from kicker import kicks
from timework import timeConversion
from dice import solve

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


cur = conn.cursor()
# cur.execute("DROP TABLE inter")
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

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('inter',))
check = (cur.fetchone()[0])
print(check)
if not check:
    cur.execute('''CREATE TABLE inter (
    NUM INT  NOT NULL,
    QUOT CHAR(200)  NOT NULL,
    TRAN CHAR(200)
    );''')
    print("Table created successfully")
    cur.execute("ALTER TABLE inter ADD CONSTRAINT test_pkey1 PRIMARY KEY (QUOT);")
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

f = open("international", "r")
f1 = f.readlines()
cnt = 0
for i in f1:
    a = i[:-1].split(' - ')
    if len(a)<2:
        a.append('')
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;",(cnt,a[0],a[1]))
    cnt += 1
    print(cnt)
cur.execute("SELECT NUM, QUOT, TRAN from inter")
rows = cur.fetchall()
for j in rows:
    print(j)

n = len(f1)
print(n)
f.close()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

bot.minutes = 0
bot.raid_id = 0
bot.account_id = 0
bot.raidlen = 25
bot.on_raid = False
bot.raidbreak = True
bot.raidstatus = 0
bot.raid_members = []

@bot.command(name='c', help="generates random quotes")
async def cook(ctx):
    cur.execute("SELECT MAX(NUM) FROM quotes;")
    r = str(cur.fetchone())
    rr = int(r[1:-2])
    print(rr)
    cur.execute("SELECT QUOT FROM quotes WHERE NUM = %s", ([random.randrange(rr + 1)]))
    resp = str(cur.fetchone())
    response = resp[2:-3].strip()
    print(response)
    await ctx.send(response)


@bot.command(name='q', help="generates random quotes with translation")
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
    print(response)
    await ctx.send(response)


@bot.command(name='w', help='Adds a quote. Use quotes around it to enter')
async def writ(ctx, line):
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

@bot.command(name='a' , help='Adds a quote. Use quotes around both quote and translation')
async def itl(ctx, line, trans =""):
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = str(cur.fetchone())
    print(a)
    if a == '(None,)':
        ar = 0
    else:
        ar = int(a[1:-2]) + 1
    print(ar)
    cur.execute("INSERT INTO inter VALUES (%s,%s,%s) ON CONFLICT (QUOT) DO NOTHING ;",(ar,line,trans))
    conn.commit()
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)


@bot.command(name='d', help='deletes last quote')
async def de(ctx):
    cur.execute("SELECT MAX(NUM) FROM inter;")
    a = int(str(cur.fetchone())[1:-2])
    print(a)
    cur.execute("DELETE FROM inter WHERE NUM = %s;",([a]))
    cur.execute("SELECT NUM, QUOT, TRAN from inter")
    rows = cur.fetchall()
    for j in rows:
        print(j)





@bot.command(name='tarot', help='')
async def tarot(ctx, variant):
    if variant == '3m':
        a = threeMajors()
        res = []
        first = []
        for q in a:
            x = printCard(q)
            first.append(x[0])
            res.append(x)
        s1 = (first[0] + ', ' + first[1] + ', ' + first[2])
        await ctx.send(s1)
        for u in res:
            s2 = (u[0] + ' - ' + u[1] + ' - ' + u[2])
            await ctx.send(s2)
    elif variant == '3k':
        a = threeCards()
        res = []
        first = []
        for q in a:
            x = printCard(q)
            first.append(x[0])
            res.append(x)
        s1 = (first[0] + ', ' + first[1] + ', ' + first[2])
        await ctx.send(s1)
        for u in res:
            s2 = (u[0] + ' - ' + u[1] + ' - ' + u[2])
            await ctx.send(s2)


@bot.command(name='deck', help='')
async def thedeck(ctx, stat, num):
    telling = fortuneTelling(stat, int(num), deckFormat())
    for s in telling:
        await ctx.send(s)


@bot.command(name='kick')
async def kick(ctx):
    a = kicks() + ctx.message.author.mention
    await ctx.send(a)

@bot.command(name = "rd", help = 'Righteous blood rolls: xd>dif - vs difficulty, xd>yd - opposed, xd>hardiness%d - damage, xd>hardiness%o - open damage')
async def rdr(ctx, line):
    a = '`'+ctx.message.author.nick+":\n"+rbroll(line)+'`'
    await ctx.send(a)

@bot.command(name = "time", help = "Converts time between timezones hh:mm Europe/Moscow Asia/Yekaterinburg")
async def time(ctx, time, zone1, zone2):
    print("time")
    message = timeConversion(time,zone1,zone2)
    print(message)
    await ctx.send(message)

@bot.command(name = "r", aliases=["roll"], help = "Rolls dice.\n kh - keeps highest, \n kl - keeps lowest \n !(limit) explodes \n <> higher/lower then limit \n >(limit)w - uses WoD rules")
async def roll (ctx, line):
    nick = ctx.message.author.nick
    if nick == None:
        nick = ctx.message.author.name
    answer = "**"+nick+":\n**" + solve(line)
    await ctx.send(answer)


@bot.command(name='raid',help='prints link to raid room',pass_context=True)
async def raid(ctx, times = '25'):
    chan = ctx.message.channel.id
    if bot.on_raid == False:
        bot.raidlen = int(times)
        message = "```WAITING FOR RAID OF " +times+  " MINUTES TO START.....```"
        sent = await ctx.send(message)
        bot.account_id = ctx.message.channel.id
        await ctx.message.delete()
        bot.raid_id = sent.id
        await sent.pin()
        bot.on_raid = True
        bot.raidbreak = True
        await sent.add_reaction("🛡️")
        await sent.add_reaction("🗡️")
        bot.raidstatus = 1

    else:
        message = "TIMER IS ALREADY ON, SEE PINNED MESSAGES"
        await ctx.send(message)
        await ctx.message.delete()


@bot.command(name='break',help='prints link to raid room',pass_context=True)
async def breaks(ctx, times = '5'):
    chan = ctx.message.channel.id
    if bot.on_raid == False:
        bot.raidlen = int(times)
        message = "```WAITING FOR BREAK OF " + times + " MINUTES TO START.....```"
        sent = await ctx.send(message)
        bot.account_id = ctx.message.channel.id
        await ctx.message.delete()
        bot.raid_id = sent.id
        await sent.pin()
        bot.on_raid = True
        bot.raidbreak = False
        await sent.add_reaction("🛏️")
        await sent.add_reaction("💤")
        bot.raidstatus = 1

    else:
        message = "TIMER IS ALREADY ON, SEE PINNED MESSAGES"
        await ctx.send(message)
        await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload):
    chan = payload.channel_id

        if payload.emoji.name == "📌":
            msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await msg.pin()
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🗡️" and payload.member.bot == False:
            print("it's alive")
            looper.start()
            bot.raidstatus = 2
            channel = bot.get_channel(bot.account_id)
            raider = await channel.fetch_message(bot.raid_id)
            remain = "```RAID IS BEGINNING: "+str(bot.raidlen-bot.minutes+1)+" MINUTES TO GO```"
            await channel.send("```RAID HAS STARTED!```")
            await raider.edit(content=remain)
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🛡️" and payload.member.bot == False:
            bot.raid_members.append(payload.member.id)
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "💤" and payload.member.bot == False:
            print("it's alive")
            looper.start()
            bot.raidstatus = 2
            channel = bot.get_channel(bot.account_id)
            raider = await channel.fetch_message(bot.raid_id)
            remain = "```BREAK WAS STARTED: " + str(bot.raidlen - bot.minutes + 1) + " MINUTES REMAINING```"
            await raider.edit(content=remain)
        elif payload.message_id == bot.raid_id and bot.raidstatus == 1 and payload.emoji.name == "🛏️" and payload.member.bot == False:
            bot.raid_members.append(payload.member.id)

@bot.event
async def on_raw_reaction_remove(payload):
    chan = payload.channel_id
    if checksetting('accountability', chan):
        if payload.emoji.name == "📌":
            print("emoji_removed")
            msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await msg.unpin()
        elif payload.message_id == bot.raid_id and (bot.raidstatus == 2 or bot.raidstatus == 1)  and payload.emoji.name == "🛡️" :
            raidmsg = await bot.get_channel(chan).fetch_message(bot.raid_id)
            reacs = raidmsg.reactions
            raiders = []
            for i in reacs:
                if i.emoji == "🛡️":
                    async for user in i.users():
                        raiders.append(user.id)
            print(raiders)
            for i in bot.raid_members:
                if i not in raiders:
                    bot.raid_members.remove(i)

            if bot.raid_members == []:
                print(bot.raid_members)
                looper.cancel()

@tasks.loop(minutes=1, count=100)
async def looper():
    if bot.minutes == bot.raidlen:
        print('DONE')
        looper.stop()
    print(bot.minutes)
    print(str(bot.raid_id), bot.account_id, "raid")
    channel = bot.get_channel(bot.account_id)
    if bot.minutes > 0:
        raider = await channel.fetch_message(bot.raid_id)
        if (bot.raidlen-bot.minutes) != 1:
            mins = " MINUTES"
        else:
            mins = " MINUTE"
        if bot.raidbreak:
            remain = "```RAID HAS "+str(bot.raidlen-bot.minutes)+mins+" TO GO```"
        else:
            remain = "```BREAK HAS "+str(bot.raidlen-bot.minutes)+" MINUTES TO GO```"
        await raider.edit(content = remain)
    bot.minutes += 1





@looper.after_loop
async def raid_done():
    print("raid done")
    bot.minutes = 0
    channel = bot.get_channel(bot.account_id)
    if bot.raidbreak:
        if bot.raid_members != []:
            message = "RAID DONE!!!\n Congratulations to "
            for user in bot.raid_members:
                member = await bot.fetch_user(user)
                name = member.mention
                message = message + name +", "
            message = message[:-2]+"!"
        else:
            message = "Sorry, everyone left"
        await channel.send (message)
        bot.raid_members = []

    else:
        message = "BREAK FINISHED!!!\n Let's go back to work, "
        for user in bot.raid_members:
            member = await bot.fetch_user(user)
            name = member.mention
            message = message + name + ", "
        message = message[:-2] + "!"
        await channel.send(message)
        bot.raid_members = []
    sent = await channel.fetch_message(bot.raid_id)
    print(sent.content)
    await sent.unpin()
    bot.on_raid = False
    bot.raidstatus = 0


bot.run(TOKEN)
