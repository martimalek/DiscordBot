from replit import db
import random

def add_forbidden_word(forbidden_word):
  if 'forbidden' in db.keys():
    forbidden = db['forbidden']
    # TODO Check that forbidden_word is not already in the db
    forbidden.append(forbidden_word)
    db['forbidden'] = forbidden
  else:
    db['forbidden'] = [forbidden_word]

def delete_forbidden_word(index):
  forbidden = db['forbidden']
  if len(forbidden) > index:
    del forbidden[index]
    db['forbidden'] = forbidden

def get_random_forbidden_word():
  if 'forbidden' in db.keys():
    forbidden = db['forbidden']
    return random.choice(forbidden)

def get_all_forbidden():
  forbidden = []
  if 'forbidden' in db.keys():
    forbidden = db['forbidden']
  else:
    print('There are no entries in the db with the "forbidden" key')
  return forbidden