latest_weather_data = {} 

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import random
from weather import current_temperature_2m
import libcst as cst
from libcst import parse_expression
import libcst.matchers as m

# update
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

class ParamUpdater(cst.CSTTransformer):
    def __init__(self, new_lat, new_lon):
        self.new_lat = new_lat
        self.new_lon = new_lon
        self.modified = False

    def leave_Assign(self, original_node, updated_node):
        if (
            isinstance(updated_node.targets[0].target, cst.Name) and
            updated_node.targets[0].target.value == "params" and
            isinstance(updated_node.value, cst.Dict)
        ):
            new_elements = []
            for element in updated_node.value.elements:
                if not isinstance(element.key, cst.SimpleString):
                    new_elements.append(element)
                    continue

                key_name = element.key.evaluated_value

                if key_name == "latitude":
                    element = element.with_changes(value=parse_expression(str(self.new_lat)))
                    self.modified = True
                elif key_name == "longitude":
                    element = element.with_changes(value=parse_expression(str(self.new_lon)))
                    self.modified = True

                new_elements.append(element)

            new_dict = updated_node.value.with_changes(elements=new_elements)
            return updated_node.with_changes(value=new_dict)

        return updated_node

@client.event
async def on_ready():
    print(f'LIFTOFF WE HAVE LIFTOFF AS {client.user}')

@client.event

async def on_message(message):
    global latest_weather_data
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Balls')
 # crime scene
    if message.content.strip().lower().startswith("$setup"):
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

            with open("weather.py", "r") as f:
                code = f.read()
            
# Parse, transform, and write back
            module = cst.parse_module(code)
            transformer = ParamUpdater(num1, num2)
            updated_module = module.visit(transformer)

            if transformer.modified:
                with open("weather.py", "w") as f:
                    f.write(updated_module.code)
                print("weather.py successfully updated.")
            else:
                print("No changes made to weather.py.")
                # STEP 2: Re-fetch using updated coordinates
            import openmeteo_requests
            import requests_cache
            from retry_requests import retry

            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": num1,
                "longitude": num2,
                "hourly": ["temperature_2m", "weather_code"],
                "models": "gfs_global",
                "current": "temperature_2m",
                "timezone": "America/Chicago",
                "minutely_15": "precipitation",
                "temperature_unit": "fahrenheit",
            }

            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            current = response.Current()
            current_temp = current.Variables(0).Value()

            latest_weather_data["location"] = (num1, num2)
            latest_weather_data["temp"] = current_temp

            await message.channel.send(f"Current temperature at `{num1}, {num2}` is **{current_temp}°F**.")
        except ValueError:
            await message.channel.send("That wasn't a valid floating-point number.")
        except asyncio.TimeoutError:
            await message.channel.send("You took too long to respond.")
        except Exception as e:
            await message.channel.send(f"Error: `{e}`")

    # --- Weather: Reuse last fetched weather info ---
    elif message.content.strip().lower().startswith("$weather"):
        if "temp" in latest_weather_data:
            lat, lon = latest_weather_data["location"]
            temp = latest_weather_data["temp"]
            await message.channel.send(f"Latest weather at `{lat}, {lon}`: **{temp}°F**")
        else:
            await message.channel.send("No weather data yet. Use `$setup` first.")

    elif message.content.startswith('$comment'):
        if "temp" in latest_weather_data:
            temp = latest_weather_data["temp"]
        if minimum < temp < maximum:
            msg_list = ["Thats light stop crying bitch enjoy the windchill.", "Ooooh shiver me timbers shut up man."]
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(random.choice(msg_list))
            # write an error message here
        if min2 < temp < max2:
            msg_list = ["They must have sent you to the 8th layer of hell with king von holy shit.", "I rather live in New Jersey bossman 😭🙏"]
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(random.choice(msg_list))
        if min3 < temp < max3:
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(f'Back in my day me and your mom used to fight 5 lions on our way to school in this weather')
        if min4 < temp < max4:
            msg_list = ["PEAK WEATHER", "Hey bro, is this paradise?", "boi if you dont close discord in 2.48583 seconds", "So ready for the public pool with the nastiest concoctions floating next to me"]
            await message.channel.send(f'{current_temperature_2m}?')
            await message.channel.send(random.choice(msg_list))
    else:
        await message.channel.send("No weather data yet. Use `$setup` first.")

@client.event
async def on_typing(channel, user, when):
    if user == client.user:
        return

    msg_list = ["GET OFF DISCORD DAWG GO OUTSIDE", "HURRY UP AND LEAVE DAMN", "STOP WRITING AN ESSAY"]

    print(f"{user} is typing message in {channel} {when}")

    if random.random() < 0.5:
        await channel.send(random.choice(msg_list))
    else:
        # Send random image
        img = discord.File("wii.png")
        await channel.send(file=img)

client.run(token)