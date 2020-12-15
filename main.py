import discord
import os
import requests
import json

client = discord.Client()

forbidden_words = ['subnormal', 'mongolo', 'retrasao']

def get_gif(query):
  response = requests.get(url = "https://api.giphy.com/v1/gifs/translate", 
  params = {'api_key': os.getenv('GIPHY_TOKEN'), 's': query})
  json_data = json.loads(response.text)['data']
  return json_data['images']['fixed_height']['url']

async def send_embed(title, desc, url, channel):
  e = discord.Embed()
  e.set_image(url=url)
  await channel.send(embed=e)

@client.event
async def on_ready():
  print('I\'ve been born as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$gif'):
    await send_embed('T', 'D', get_gif('magic'), message.channel) # Make this depend on the second word of the message `$gif magic`

  if msg.startswith('$bot'):
    await message.channel.send('F*ck you!')

  if any(word in msg for word in forbidden_words):
    await message.channel.send('A mi no me insultes eh')
    # await message.channel.send('{0} tu madre!'.format(word))

client.run(os.getenv('DISCORD_TOKEN'))