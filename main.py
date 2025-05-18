import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from weather import current_temperature_2m, minutely_15_dataframe, hourly_dataframe, hourly_temperature_2m, hourly, hourly_data, hourly_weather_code

# update
# if current_temp > 50, then "get ur ass outside lmao"

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
	if message.content.startswith('$weather'):
		await message.channel.send(f'Weather: {current_temperature_2m}')


client.run(token)

