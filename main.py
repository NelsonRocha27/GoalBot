import discord
import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from discord.ext import commands

# client = discord.Client()
client = commands.Bot(command_prefix='.')

load_dotenv()

cluster = MongoClient(os.getenv('DBURL'))
db = cluster["GoalBotDB"]
collection = db["Teams"]


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
    guildIDQuery = {"_id": ctx.guild.id}
    if collection.count_documents(guildIDQuery) == 0:
        post = {"_id": ctx.guild.id, "team": [team]}
        collection.insert_one(post)
    else:
        guild = collection.find(guildIDQuery)
        for result in guild:
            listOfTeams = result["team"]
        listOfTeams.append(team)
        collection.update_one({"_id": ctx.guild.id}, {"$set": {"team": listOfTeams}})


@client.command(aliases=['list'])
async def list_teams(ctx):
    listOfTeams = []
    for document in collection.find({"_id": ctx.guild.id, "team": {"$exists": True}}):
        listOfTeams = document['team']

    if len(listOfTeams) > 0:
        await ctx.send("\n".join(listOfTeams))
    else:
        await ctx.send("There no teams in database.")


client.run(os.getenv('TOKEN'))
