import discord
import os

from keep_alive import keep_alive
from giphy import get_gif_by_query, get_random_gif
from persistance import get_random_forbidden_word, add_forbidden_word, get_all_forbidden, add_summoner
from rito import get_summoner_by_name
from exceptions import SummonerAlreadyInDb, ForbiddenWordAlreadyInDb

client = discord.Client()

forbidden_words = get_all_forbidden()

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
          await send_embed(
              get_gif_by_query(msg.split('$gif ', 1)[1]), message.channel)

    if msg.startswith('$insult'):
      new_forbidden_word = msg.split('$insult ', 1)[1]
      try:
        add_forbidden_word(new_forbidden_word)
        await message.channel.send(f'Gracias <3 {get_random_forbidden_word()}.')
      except ForbiddenWordAlreadyInDb:
        await message.channel.send(f'No te repitas {get_random_forbidden_word()}.')

    if msg.startswith('$del'):
      if len(words) > 1:
        index = int(words[1])
        print(index)
      else:
        await message.channel.send('Debes especificar un número después del comando $del.')

    if msg.startswith('$list'):
        await message.channel.send(get_all_forbidden())

    if msg.startswith('$add'):
      summoner_name = msg.split('$add ', 1)[1]
      summoner_info = get_summoner_by_name(summoner_name)
      if 'id' in summoner_info.keys():
        try:
          add_summoner(summoner_name, summoner_info)
        except SummonerAlreadyInDb:
          await message.channel.send('Este invocador ya ha sido añadido.')
        except:
          print('Exception thrown!')
      else:
        await message.channel.send(f'No he encontrado al invocador {summoner_name}.')

    if any(word in msg for word in forbidden_words):
        await message.channel.send('A mi no me insultes eh {0}'.format(
            get_random_forbidden_word()))

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
