import random
from replit import db
from exceptions import SummonerAlreadyInDb, ForbiddenWordAlreadyInDb, SummonerNotInDb

SUMMONERS_DB_KEY = 'summoners'
FORBIDDEN_DB_KEY = 'forbidden'

def add_forbidden_word(forbidden_word):
  if FORBIDDEN_DB_KEY in db.keys():
    forbidden = db[FORBIDDEN_DB_KEY]
    if forbidden_word in forbidden:
      raise ForbiddenWordAlreadyInDb
    forbidden.append(forbidden_word)
    db[FORBIDDEN_DB_KEY] = forbidden
  else:
    db[FORBIDDEN_DB_KEY] = [forbidden_word]

def delete_forbidden_word(index):
  forbidden = db[FORBIDDEN_DB_KEY]
  if len(forbidden) > index:
    del forbidden[index]
    db[FORBIDDEN_DB_KEY] = forbidden

def get_random_forbidden_word():
  if FORBIDDEN_DB_KEY in db.keys():
    forbidden = db[FORBIDDEN_DB_KEY]
    return random.choice(forbidden)

def get_all_forbidden():
  forbidden = []
  if FORBIDDEN_DB_KEY in db.keys():
    forbidden = db[FORBIDDEN_DB_KEY]
  else:
    print('There are no entries in the db with the "forbidden" key')
  return forbidden

def add_summoner(summoner_name, summoner_info):
  print('add_summoner', summoner_name, summoner_info)
  if SUMMONERS_DB_KEY in db.keys():
    summoners = db[SUMMONERS_DB_KEY]
    if summoner_name in summoners.keys():
      raise SummonerAlreadyInDb
    summoners[summoner_name] = summoner_info
    print(f'summoner {summoner_name} added ')
    db[SUMMONERS_DB_KEY] = summoners
  else:
    db[SUMMONERS_DB_KEY] = {summoner_name:summoner_info}

def delete_summoner(summoner_name):
  print('delete_summoner', summoner_name)
  if SUMMONERS_DB_KEY in db.keys():
    summoners = db[SUMMONERS_DB_KEY]
    if summoner_name in summoners.keys():
      del summoners[summoner_name]
      db[SUMMONERS_DB_KEY] = summoners
    else:
      raise SummonerNotInDb

def get_summoners():
  if SUMMONERS_DB_KEY in db.keys():
    return db[SUMMONERS_DB_KEY]
  else:
    return {}