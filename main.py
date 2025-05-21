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

a = 20
b = 60

minimum = min(a, b)
maximum = max(a, b)

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
	if message.content.startswith('$comment'):
		if minimum < current_temperature_2m < maximum:
			await message.channel.send(f'{current_temperature_2m}? Thats light stop crying bitch enjoy the windchill.')
			# write an error message here


		# if message.content.startswith('$comment'):
	 #   if current_temperature_2m < 20:
	 #   	await message.channel.send(f'{current_temperature_2m}? Thats light stop crying bitch enjoy the windchill.')
	 #   if current_temperature_2m < 50:
	 #   	await message.channel.send(f'{current_temperature_2m}? The woke mob will tel you a sweater is needed, but I don"t buy it')
	 #   if current_temperature_2m < 80:
	 #   	await message.channel.send(f'{current_temperature_2m}? Zamn that is scorching')



client.run(token)

