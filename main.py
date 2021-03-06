import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import asyncio
import coupons_scraper

client = discord.Client()
sad_words = ["sad", "depressed", "unhappy", "miserable", "mournful", "hopeless", "despairing", "downcast", "gloomy", "heartbroken", "melancholy", "pessimistic", "somber", "worry", "wistful", "dismal" "bitter" ]

starter_encouragements = [
  "Cheer up!",
   "You are strong",
   "Life has these thorns says the book",
   "Failure is simply the oppurtunity to begin again", "FAIL stands for First Attempt In Learning",
    "If you are feeling helpless, help others", 
    "Never do what your rivals expect you to do", 
    "Hang in there",
    "Code for a while, and you will know what happiness is",
    "We can do no great things, only small things with great love",
    "Life shrinks or expands in proportion with one’s courage, so never lose it within a defeat",
    "You may not be perfect, but parts of you are pretty awesome",
    "I know for sure that what you dwell on is what you become",
    "Kick-start your personal growth if you're in a rut",
    "It does not matter if you walk slow as long as you do not stop",
    "I can see you're really trying",
    "You have been assigned to this task to show that this mountain can be moved"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

async def send_messages():
        await client.wait_until_ready()
        for guild in client.guilds:
            for channel in guild.channels:
                if "coupons" in channel.name:
                    coupons = coupons_scraper.fetch_coupons()
                    for message in coupons:
                        await channel.send(message)
                        await asyncio.sleep(2)
        await asyncio.sleep(14400)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(
                          type=discord.ActivityType.watching,
                          name='depressed people become encouraged'))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg == 'hop!inspire':
    quote = get_quote()
    embed = discord.Embed(title=quote, colour=0xccdd)
    await message.channel.send(content=None, embed=embed)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.append(db["encouragements"])

    if any(word in msg.split(" ") for word in sad_words):
        embed = discord.Embed(title=random.choice(options), colour=0xccdd)
        await message.channel.send(content=None, embed=embed)

  if msg.startswith("hop! new"):
    encouraging_message = msg.split("hop! new ",1)[1]
    update_encouragements(encouraging_message)
    embed = discord.Embed(title="New encouraging message added.", colour=0xccdd)
    await message.channel.send(content=None, embed=embed)   

  if msg.startswith("hop! del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("hop! del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    embed = discord.Embed(title=encouragements, colour=0xccdd)
    await message.channel.send(content=None, embed=embed)   

  if msg == "hop! list":
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    embed = discord.Embed(title=encouragements, colour=0xccdd)
    await message.channel.send(content=None, embed=embed)  

  if msg.startswith("hop! responding"):
    value = msg.split("hop! responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      embed = discord.Embed(title="You have turned off responses.", colour=0xccdd)
      await message.channel.send(content=None, embed=embed)  
    else:
      db["responding"] = False
      embed = discord.Embed(title="You have turned on responses.", colour=0xccdd)
      await message.channel.send(content=None, embed=embed) 


      

keep_alive()
client.loop.create_task(send_messages())
client.run(os.getenv('Pass'))