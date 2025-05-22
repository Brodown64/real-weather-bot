import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from weather import current_temperature_2m, minutely_15_dataframe, hourly_dataframe, hourly_temperature_2m, hourly, hourly_data, hourly_weather_code

# update
# prompt ideas: "I rather live in New Jersey bossman 😭🙏"
# on typing event: GET OFF DISCORD DAWG GO OUTSIDE, the wii take a break image

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

a = 20
b = 60
c = 80
d = 110
e = 0 
f = 40

minimum = min(a, b)
maximum = max(a, b)

min2 = min(c, d)
max2 = max(c, d)

min3 = min(e, a)
max3 = max(e, a)

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
			msg_list = ["Thats light stop crying bitch enjoy the windchill.", "Ooooh shiver me timbers shut up man."]
			await message.channel.send(f'{current_temperature_2m}?')
			await message.channel.send(random.choice(msg_list))
			# write an error message here
		if min2 < current_temperature_2m < max2:
			await message.channel.send(f'They must have sent you to the 8th layer of hell with king von holy shit.')
		if min3 < current_temperature_2m < max3:
			await message.channel.send(f'Back in my day me and your mom used to fight 5 lions on our way to school in this weather')

		# if minimum < current_temperature_2m < maximum:
		# 	await message.channel.send(f'{current_temperature_2m}? Thats light stop crying bitch enjoy the windchill.')
		# 	# write an error message here
		# if min2 < current_temperature_2m < max2:
		# 	await message.channel.send(f'They must have sent you to the 8th layer of hell with king von holy shit.')
		# if min3 < current_temperature_2m < max3:
		# 	await message.channel.send(f'Back in my day me and your mom used to fight 5 lions on our way to school in this weather')



client.run(token)