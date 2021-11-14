import discord
import os
import pymongo
from database import DataBase
from dotenv import load_dotenv
from discord.ext import commands

# client = discord.Client()
client = commands.Bot(command_prefix='.')

load_dotenv()

db = DataBase(os.getenv('DBURL'))

@client.event
async def on_ready():
    print('Bot is now logged in as {0.user}'
          .format(client))


"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
"""


@client.command()
async def ping(ctx):
    await ctx.send('pong')


@client.command(aliases=['add'])
async def add_team(ctx, team):
    db.Add_Team(ctx.guild.id, team)


@client.command(aliases=['list'])
async def list_teams(ctx):
    if db.List_Teams(ctx.guild.id) is True:
        await ctx.send(db.listOfTeams)
    else:
        await ctx.send("There no teams in database.")


client.run(os.getenv('TOKEN'))
