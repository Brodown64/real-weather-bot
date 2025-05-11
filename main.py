import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os 

# update
# find an outside source to pull weather

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'LIFTOFF WE HAVE LIFTOFF AS {client.user}')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Balls')

client.run(token)

