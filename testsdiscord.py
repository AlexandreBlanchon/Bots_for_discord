# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 19:07:12 2018

@author: Alexandre
"""


import discord.ext.commands as disc
import os


TOKEN = os.environ['TOKEN']
PREFIX = os.environ['PREFIX']
client = disc.Bot(command_prefix = PREFIX)
    
@client.command()
async def hello():
    await client.say("Hello !")
    
client.run(TOKEN)

