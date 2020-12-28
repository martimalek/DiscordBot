import discord
import os
from discord.ext import tasks

from keep_alive import keep_alive
from giphy import get_gif_by_query, get_random_gif
from persistance import get_random_forbidden_word, add_forbidden_word, get_all_forbidden, add_summoner, get_summoners, delete_summoner
from rito import get_summoner_by_name, get_current_match_by_summoner_id
from exceptions import SummonerAlreadyInDb, ForbiddenWordAlreadyInDb, SummonerNotInDb

client = discord.Client()

forbidden_words = get_all_forbidden()
summoners_in_match = []

async def on_gif_message(message):
  if len(message.content.split(sep=None)) == 1:
      await send_embed(get_random_gif(), message.channel)
  else:
      await send_embed(
          get_gif_by_query(message.content.split('$gif ', 1)[1]), message.channel)

async def on_insult_message(message):
  try:
    add_forbidden_word(message.content.split('$insult ', 1)[1])
    await message.channel.send(f'Gracias <3 {get_random_forbidden_word()}.')
  except ForbiddenWordAlreadyInDb:
    await message.channel.send(f'No te repitas {get_random_forbidden_word()}.')

async def on_del_message(message):
  try:
    summoner_to_delete = message.content.split('$del ', 1)[1]
    if len(summoner_to_delete) < 1:
      raise Exception()
  except:
    print('Command is missing name')
    await message.channel.send('Debes especificar un nombre de invocador después del comando.')
  try:
    delete_summoner(summoner_to_delete)
    await message.channel.send(f'Deleting {summoner_to_delete}')
  except SummonerNotInDb:
    await message.channel.send('El invocador no está guardado.')

async def on_list_message(message):
  await message.channel.send(get_all_forbidden())

async def on_add_message(message):
  summoner_name = message.content.split('$add ', 1)[1]
  summoner_info = get_summoner_by_name(summoner_name)
  if 'id' in summoner_info.keys():
    try:
      add_summoner(summoner_name, summoner_info)
      await message.channel.send(f'Invocador {summoner_name} añadido correctamente.')
    except SummonerAlreadyInDb:
      await message.channel.send('Este invocador ya ha sido añadido.')
  else:
    await message.channel.send(f'No he encontrado al invocador {summoner_name}.')

async def on_help_message(message):
  await message.channel.send('Te va a ayudar tu puta madre...')

on_message_dict = {
  '$gif': on_gif_message,
  '$insult': on_insult_message,
  '$del': on_del_message,
  '$list': on_list_message,
  '$add': on_add_message,
  '$help': on_help_message,
}

async def send_embed(url, channel):
    e = discord.Embed()
    e.set_image(url=url)
    await channel.send(embed=e)

@tasks.loop(seconds=30)
async def check_match_ended():
  print('Checking if match ended...')
  if len(summoners_in_match) > 0:
    finished_summoners = []
    summoners = get_summoners()
    for summoner in summoners_in_match:
      current_match = get_current_match_by_summoner_id(summoners[summoner]['id'])
      if 'participants' not in current_match.keys():
        finished_summoners.append(summoner)
        print(f'Match finished {summoner}')

    print(finished_summoners)
    for summoner in finished_summoners:
      summoners_in_match.remove(summoner)
      await send_message_to_general(f'El invocador {summoner} ha terminado la partida.')
    print(finished_summoners)

@tasks.loop(minutes=5)
async def check_summoners():
  print('Checking summoners...')
  summoners = get_summoners()
  for summoner_name in summoners.keys():
    current_match = get_current_match_by_summoner_id(summoners[summoner_name]['id'])
    if 'participants' in current_match.keys():
      for participant in current_match['participants']:
        if participant['summonerName'] == summoner_name and summoner_name not in summoners_in_match:
          summoners_in_match.append(summoner_name)
          print(f'{summoner_name} found in match')
    else:
      print(f'{summoner_name} is not in a match')

async def send_message_to_general(message):
  all_channels = client.get_all_channels()
  general = None
  for channel in all_channels:
    if channel.name == 'general':
      general = channel
  if general:
    await general.send(message)

@client.event
async def on_ready():
  print('I\'ve been born as {0.user}'.format(client))
  check_match_ended.start()
    
@client.event
async def on_message(message):
    if message.author == client.user:
      return

    command = message.content.split(sep=None)[0]

    if command in on_message_dict.keys():
      print(f'command [{command}] found')
      await on_message_dict[command](message)

    if any(word in message.content for word in forbidden_words):
        await message.channel.send('A mi no me insultes eh {0}'.format(
            get_random_forbidden_word()))

check_summoners.start()
keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
