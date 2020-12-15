import discord
import os

client = discord.Client()

forbidden_words = ['subnormal', 'mongolo', 'retrasao']

@client.event
async def on_ready():
  print('I\'ve been born as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$bot'):
    await message.channel.send('F*ck you!')

  # any(word in msg for word in forbidden_words)
  if any(word in msg for word in forbidden_words):
    await message.channel.send('A mi no me insultes eh')
    # await message.channel.send('{0} tu madre!'.format(word))

client.run(os.getenv('DISCORD_TOKEN'))