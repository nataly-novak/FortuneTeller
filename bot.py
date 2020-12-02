import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
f = open("quotes.txt", "r")
f1 = f.readlines()
n = len(f1)
print(n)
f.close()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='c', help = "generates random quotes")
async def cook(ctx):
    print(len(f1))
    response = str(f1[random.randrange(len(f1))])
    print(len(f1))
    await ctx.send(response)

@bot.command(name='w' , help='Adds a quote. Use quotes around')
async def writ(ctx, line):
    ff = open("quotes.txt", "a+")
    ff.write(line)
    ff.write("\n")
    ff.close()
    f1.append(line)
    print(len(f1))


bot.run(TOKEN)