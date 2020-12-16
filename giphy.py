import requests
import json
import os

def get_gif_by_query(query):
  response = requests.get(url = "https://api.giphy.com/v1/gifs/translate", 
  params = {'api_key': os.getenv('GIPHY_TOKEN'), 's': query})
  json_data = json.loads(response.text)['data']
  return json_data['images']['fixed_height']['url']

def get_random_gif():
  response = requests.get(url = "https://api.giphy.com/v1/gifs/random", 
  params = {'api_key': os.getenv('GIPHY_TOKEN')})
  json_data = json.loads(response.text)['data']
  return json_data['images']['fixed_height']['url']