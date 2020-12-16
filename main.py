import discord
import os
import random

from giphy import get_gif_by_query, get_random_gif
from persistance import get_random_forbidden_word, add_forbidden_word

client = discord.Client()

forbidden_words = ['subnormal', 'mongolo', 'retrasao']

async def send_embed(url, channel):
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
  words = msg.split(sep=None)

  if msg.startswith('$gif'):
    if len(words) == 1:
      await send_embed(get_random_gif(), message.channel)
    else:
      await send_embed(get_gif_by_query(words[1]), message.channel)

  if msg.startswith('$insult'):
    new_forbidden_word = msg.split('$insult ', 1)[1]
    add_forbidden_word(new_forbidden_word)

    await message.channel.send('Gracias por tu insulto <3 {0}'.format(get_random_forbidden_word()))


  if any(word in msg for word in forbidden_words):
    await message.channel.send('A mi no me insultes eh')
    await message.channel.send(get_random_forbidden_word())
    # await message.channel.send('{0} tu madre!'.format(word))

client.run(os.getenv('DISCORD_TOKEN'))