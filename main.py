import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import random
import numpy as np
import asyncio
import config

intents = discord.Intents.default()
intents.message_content = True

guild = discord.Object(id=config.server_id)
class aclient(discord.Client):
    def __init__(self):
        super().__init__(command_prefix=config.prefix, intents = intents)
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced
            await tree.sync(guild = guild) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

bot=aclient()
tree = app_commands.CommandTree(bot)
@tree.command(guild = guild, name = 'roll', description='Кинуть специальную кость')
async def roll(ctx: discord.Interaction,грани: int, бросков:int = 1):
    throws=бросков
    dice=грани+1
    if dice<2:
        dice=2
    if throws<1:
        throws=1
    if throws==1:
        await ctx.response.send_message("["+str(грани)+"] "+str(random.randint(1, dice-1)))
    else:
        await ctx.response.send_message("["+str(грани)+"] "+roll(dice, throws))
#@tree.command(guild = guild, name = 'd4', description='Кинуть d4')
#async def d4(ctx: discord.Interaction,бросков:int = 1):
#    throws=бросков
#    dice=5
#    if throws<1:
#        throws=1
#    if throws==1:
#        await ctx.response.send_message(str(random.randint(1, dice)))
#    else:
#        await ctx.response.send_message(roll(dice, throws))
#@tree.command(guild = guild, name = 'd6', description='Кинуть d6')
#async def d6(ctx: discord.Interaction,бросков:int = 1):
#    throws=бросков
#    dice=7
#    if throws<1:
#        throws=1
#    if throws==1:
#        await ctx.response.send_message(str(random.randint(1, dice)))
#    else:
#        await ctx.response.send_message(roll(dice, throws))
#
#@tree.command(guild = guild, name = 'd20', description='Кинуть d20')
#async def d20(ctx: discord.Interaction,бросков:int = 1):
#    throws=бросков
#    dice=21
#    if throws<1:
#        throws=1
#    if throws==1:
#        await ctx.response.send_message(str(random.randint(1, dice)))
#    else:
#        await ctx.response.send_message(roll(dice,throws))

def roll(dice:int,throws:int):
    if throws < 100:
        dices = np.random.randint(1, dice, throws)
        text = str(dices[0])
        for i in range(1, len(dices)):
            text += '+' + str(dices[i])
        text += '=' + str(dices.sum())
        return text
    else:
        dices = np.random.randint(1, dice, throws)
        return str(dices.sum())

@bot.event
async def on_thread_create(thread):
    if thread.parent_id ==1047386949280874557: #лента1
        lenta = bot.get_channel(1047387062531276810)
    elif thread.parent_id ==1047387006969327628:#лента 2
        lenta = bot.get_channel(1047387096031186985)
    elif thread.parent_id ==1044000947845734490:#творческая лента
        lenta = bot.get_channel(1047507449395040277)
    elif thread.parent_id ==1044005454302433280:#спонсорская лента
        lenta = bot.get_channel(1047508309797773392)
    else:
        lenta = bot.get_channel(1047387916030201907)
    def check(m):
        return m.channel.id == thread.id

    try:
        m =await bot.wait_for('message', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        print("нет сообщения в"+thread.name)
    else:
        message = thread.starter_message
        files: list[discord.File] = []
        for img in message.attachments:
            file = await img.to_file()
            files.append(file)
        text ="**"+thread.name + "** \n"
        text += message.content
        button = Button(label="Обсуждение", style=discord.ButtonStyle.url, url=thread.jump_url)
        view = View()
        view.add_item(button)
        mess = await lenta.send(text, view=view, files=files)
        emojis = ['<:Yana_good_girl:1035648507891175495>' ,'<:__:1035663881307176991>','<:D_:1035663877909794907>','<:cat_hor:1035663875963621386>']
        for emo in emojis:
            await mess.add_reaction(emo)



bot.run(config.TOKEN)
