''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import os
import sys
import json
from typing import Optional, Dict, List
from pathlib import Path

# -- 3rd party libararies -- #
from pydantic import BaseModel

# -- base classes that are used to validate the config -- #
class Token(BaseModel):
  token: str

class Embeds(BaseModel):
  title = 'Buy Zeus for yourself today!'
  description = 'Advanced Customizable Selfbot'
  author = 'Authors: k1rk & Charge'
  author_url: Optional[str] = None
  footer = 'Zeus Selfbot Inc. (c)'
  footer_url: Optional[str] = None
  image_url: Optional[str] = None
  link: Optional[str] = None
  thumbnail: Optional[str] = None
  delete_after = 5
  color = 0x000000

class Bot(BaseModel):
  name = 'Zeus Selfbot'
  prefix = '.'
  token: str
  presence = False
  sniper = False
  delete = False
  log = False

class Presence(BaseModel):
  state = 'Zeus - Coming Soon'
  details = 'Advanced Selfbot'
  hover_big = 'DM .k#1999 or charge#0666'
  hover_small = 'Zeus Selfbot'
  
class Logging(BaseModel):
  keywords: List[str]
  user_ids: List[int]
  guild_ids: List[int]

# -- main class for holding the config -- #
class Config:
  log = None
  rp = None
  token = None
  embeds = None
  bot = None

# -- Main class used to load the config -- #
class Loader:
  '''
  class that opens json config 
  loads it in and validates that each value
  is correct
  '''
  def __init__(self, filename):
    self.filename = filename

  @classmethod
  def die(cls, info, e):
    print(
      f'Zeus Selfbot (c)\n'
      f'Info: {info if info else "nil"}\n'
      f'Error: {getattr(e, "message", repr(e)) if e else "nil"}',
      file=sys.stderr
    )
    sys.exit(-1)
  
 
  def get_config(self):
    # check if file is there
    if not self.filename.exists():
      Loader.die(
        f'Config File: {self.filename}, Could not be found in local dir', 
        None
      )
    
    # attempt to open the file
    try:
      with open(self.filename, 'r') as cf:
        config = json.load(cf)
    except Exception as e:
      Loader.die(
        f'Could Not Open File and or Read File Into Json Format', 
        e
      )
    
    # return config
    return config
  
  def load_config(self):

    # grab json
    data = self.get_config()
    
    # check that base keys exist
    if any(
      data.get(x) is None for x in (
        'logging', 'embeds', 
        'presence', 'bot'
      )
    ):
      Loader.die(
        f'Missing Key In Json Config File: [{self.filename}]',
        None
      )
     
    # fill out config 
    config = Config()
    config.embeds = Embeds(**data['embeds'])
    config.bot = Bot(**data['bot'])
    config.rp = Presence(**data['presence'])
    config.log = Logging(**data['logging'])
     
    # return new config
    return config
