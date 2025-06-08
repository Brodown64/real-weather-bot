import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import random
from weather import current_temperature_2m, minutely_15_dataframe, hourly_dataframe, hourly_temperature_2m, hourly, hourly_data, hourly_weather_code

# update
# find a new way to change weather cuz this is too hard lmao
# prompt ideas: "I rather live in New Jersey bossman 😭🙏"
# on typing event: GET OFF DISCORD DAWG GO OUTSIDE, HURRY UP AND LEAVE DAMN, STOP WRITING AN ESSAY, the wii take a break image
# facts about weather, post history on weather disasters
# count how many times people chat in the server, and make a I haven't touched grass leaderboard and add some roles
# the thumbnail being like "hey whats the weather" and the bot responding with "KILL YOURSELF"
# play nature noises in VC

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

min3 = min(e, a) # 0 to 20
max3 = max(e, a)

minimum = min(a, b) # 20 to 60
maximum = max(a, b)

min4 = min(b, c) # 60 to 80
max4 = max(b, c)

min2 = min(c, d) # 80 to 110
max2 = max(c, d)

@client.event
async def on_ready():
    print(f'LIFTOFF WE HAVE LIFTOFF AS {client.user}')

@client.event

async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Balls')
 # crime scene
    if message.content.strip().lower().startswith("$askfloats"):
        await message.channel.send("Please enter a floating-point number:")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            reply = await client.wait_for("message", timeout=30.0, check=check)
            parts = reply.content.strip().split()

            if len(parts) != 2:
                await message.channel.send("You need to enter exactly two numbers.")
                return

            num1 = float(parts[0])
            num2 = float(parts[1])
            await message.channel.send(f"You entered: `{num1}` and `{num2}`")
        except ValueError:
            await message.channel.send("That wasn't a valid floating-point number.")
        except asyncio.TimeoutError:
            await message.channel.send("You took too long to respond.")
  # crime scene

    if message.content.startswith('$weather'):
        await message.channel.send(f'Weather: {current_temperature_2m}')

    if message.content.startswith('$comment'):
        if minimum < current_temperature_2m < maximum:
            msg_list = ["Thats light stop crying bitch enjoy the windchill.", "Ooooh shiver me timbers shut up man."]
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(random.choice(msg_list))
            # write an error message here
        if min2 < current_temperature_2m < max2:
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(f'They must have sent you to the 8th layer of hell with king von holy shit.')
        if min3 < current_temperature_2m < max3:
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(f'Back in my day me and your mom used to fight 5 lions on our way to school in this weather')
        if min4 < current_temperature_2m < max4:
            msg_list = ["PEAK WEATHER", "Hey bro, is this paradise?", "boi if you dont close discord in 2.48583 seconds", "So ready for the public pool with the nastiest concoctions floating next to me"]
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(random.choice(msg_list))


client.run(token)