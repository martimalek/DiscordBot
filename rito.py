import requests
import json
import os

def get_summoner_by_name(name):
  response = requests.get(url = 
  f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={os.getenv('RITO_TOKEN')}")
  return json.loads(response.text)

def get_current_match_by_summoner_id(summoner_id):
  response = requests.get(url = 
  f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={os.getenv('RITO_TOKEN')}")
  return json.loads(response.text)