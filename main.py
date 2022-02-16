import asyncio
import os
from database import DataBase
from twitter import Twitter
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

# client = discord.Client()
client = commands.Bot(command_prefix='.')
db = DataBase(os.getenv('DBURL'))
twitterApps = []
screenNames = ['SPORTTVPortugal', 'ElevenSports_PT']


@client.event
async def on_ready():
    for guild in client.guilds:
        twitter = Twitter(screenNames)
        twitter.Set_Guild_Id(guild.id)
        twitter.Set_List_Of_Keywords(db.Get_List_Teams(guild.id))
        text_channel_id = db.Get_Text_Channel(guild.id)
        if text_channel_id is not None:
            twitter.Set_Text_Channel_ID(text_channel_id)
        else:
            text_channel_list = []
            for channel in guild.text_channels:
                text_channel_list.append(channel.id)
            twitter.Set_Text_Channel_ID(text_channel_list[0])
        twitterApps.append(twitter)
        print('Bot listening for goals in {0}'.format(guild.name))
    print('Bot is now logged in as {0.user}'.format(client))


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
    for twitterApp in twitterApps:
        if twitterApp.Get_Guild_Id() == ctx.guild.id:
            twitterApp.Set_List_Of_Keywords(db.Get_List_Teams(ctx.guild.id))


@client.command(aliases=['list'])
async def list_teams(ctx):
    if db.List_Teams(ctx.guild.id):
        await ctx.send(db.Get_List_Teams_As_String(ctx.guild.id))
    else:
        await ctx.send("There are no teams in database.")


@client.command(aliases=['here'])
async def set_text_channel(ctx):
    for twitterApp in twitterApps:
        if twitterApp.Get_Guild_Id() == ctx.guild.id:
            twitterApp.Set_Text_Channel_ID(ctx.channel.id)
    db.Define_Text_Channel(ctx.guild.id, ctx.channel.id)


async def my_background_task():
    await client.wait_until_ready()
    message_link = None

    while not client.is_closed():
        # print("lol")

        for twitterApp in twitterApps:

            if twitterApp.Get_New_Tweet():

                if twitterApp.Get_Text_Channel_ID() is not None:
                    channel = client.get_channel(twitterApp.Get_Text_Channel_ID())  # channel ID goes here
                else:
                    text_channel_list = []
                    for guild in client.guilds:
                        if guild.id == twitterApp.Get_Guild_Id():
                            for channel in guild.text_channels:
                                text_channel_list.append(channel)
                    channel = text_channel_list[0]

                await channel.send(twitterApp.Get_Tweet_Link())
                twitterApp.Set_New_Tweet(False)

        await asyncio.sleep(1)  # task runs every 1 second


def some_function():
    while True:
        for twitterApp in twitterApps:
            if twitterApp.Get_New_Tweet():
                channel = client.channels.fetch(twitterApp.Get_Guild_Id())
                channel.send(db.Get_List_Teams_As_String(twitterApp.Get_Guild_Id()))
                twitterApp.Set_New_Tweet(False)


client.loop.create_task(my_background_task())
client.run(os.getenv('TOKEN'))
pass
