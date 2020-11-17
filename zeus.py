''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import sys
import os
from time import sleep
import logging
from pathlib import Path
import json

# -- 3rd party libararies -- #
import discord
from discord.ext import commands
from pypresence import Presence

# -- local libraries -- #
from config import Loader
from embeds import Embeds

# -- Globals and Constants -- #
LOG_LEVEL = logging.INFO
LOG_DATE_FMT = '%d/%m/%Y %I:%M %p'
LOG_SEP_STRING = '\n-------------------------------\n'
LOG_FMT = LOG_SEP_STRING[1:] + 'Time: %(asctime)s\nLevel: %(levelname)s\nName: %(name)s\nData: %(message)s' + LOG_SEP_STRING
LOG_DIREC = Path('./logs')
SETTINGS_DIREC = Path('./settings')
CONFIG_FILE = SETTINGS_DIREC / 'zeus.config.json'
ERROR_FILE_NAME =  LOG_DIREC  / 'zeus.errors.log'
MESSAGE_LOG_FILE_NAME = LOG_DIREC / 'zeus.message-log.json'
CLIENT_ID = ''


# -- main class -- #
class Zeus(commands.Bot):
  '''
  simple class that inherits from commands.Bot
  '''
  
  def __init__(self, filename):
    self.rp = Presence(CLIENT_ID)
    self.config_file_name = filename
    self.config = None
    self.embeds = None
    self.i = 0

  def load_config(self):
    # load the config and load the embeds
    self.config = Loader(self.config_file_name).load_config()
    self.embeds = Embeds(self.config)
  
  def load_rp(self):

    # check if presence is set to true in the config file
    if self.config.bot.presence:

      # connect and update to config file values
      self.rp.connect()
      self.rp.update(
        state=self.config.rp.state,
        details=self.config.rp.details,
        large_image='big',
        small_image='small',
        small_text=self.configr.rp.hover_small,
        large_text=self.config.rp.hover_big
      )

  def init_error_n_message_log(self):
    
    # -- init the error log file -- # 
    logging.getLogger('discord').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('pypresence').setLevel(logging.ERROR)

    # -- make sure direcotory exists -- #
    if not LOG_DIREC.exists():
      os.mkdir(LOG_DIREC)
    elif not LOG_DIREC.is_dir():
      os.remove(LOG_DIREC)
      os.mkdir(LOG_DIREC)

    # -- init the error file -- #
    if not ERROR_FILE_NAME.exists():
      open(ERROR_FILE_NAME, 'w+').close()
    elif not ERROR_FILE_NAME.is_file():
      os.remove(ERROR_FILE_NAME)
      open(ERROR_FILE_NAME, 'w+').close()

    # -- init the messsage log file -- #
    if not MESSAGE_LOG_FILE_NAME.exists():
      open(MESSAGE_LOG_FILE_NAME, 'w+').close()
    elif not MESSAGE_LOG_FILE_NAME.is_file():
      os.remove(MESSAGE_LOG_FILE_NAME)
      open(MESSAGE_LOG_FILE_NAME, 'w+').close()

    # set the logging config
    logging.basicConfig(
      level=LOG_LEVEL,
      filename=ERROR_FILE_NAME,
      datefmt=LOG_DATE_FMT,
      format=LOG_FMT
    )

  def log_init(self):
    with open(MESSAGE_LOG_FILE_NAME, 'w') as f:
      json.dump({}, f, indent=2)

  def new_log(self, data):
    self.i += 1
    # get data
    with open(MESSAGE_LOG_FILE_NAME, 'r') as fo:
      yes = json.load(fo)
    
    # update
    x = {f'message: {self.i}': data}
    yes.update(x)
      
    # rewrite
    with open(MESSAGE_LOG_FILE_NAME, 'w') as f:
      json.dump(yes, f, indent=2)
      
  def get_cogs(self):
    return [
      f'cogs.{x[:-3]}' for x in os.listdir('./cogs')
      if x.endswith('.py')
    ]
  
  def _load(self):
    for cog in self.get_cogs():
      super().load_extension(cog)

  def _unload(self):
    for cog in self.get_cogs():
      super().unload_extension(cog)
  
  def refresh(self):
    self._unload()
    self._load()

  def init(self):

    # load config and init error log
    self.load_config()
    self.init_error_n_message_log()
    self.log_init()
    
    # call the clients init method with desired config
    super().__init__(
      description=self.config.bot.name, 
      command_prefix=self.config.bot.prefix, 
      self_bot=True
    )

    # load all the cogs
    self._load()
    
    if os.name == 'nt':
      # load rp
      self.load_rp()

  def go(self):
    super().remove_command('help')
    super().run(self.config.bot.token, bot=False)
    
# -- create a new bot instance -- #
bot = Zeus(CONFIG_FILE)
bot.init()

# -- base commands for the bot -- #
@bot.command(name='reload', aliases=['refresh', 'reset', 'restart', 'onoff'])
async def reload(ctx):
  
  # load config reload cogs and delete original message
  bot.load_config()
  if bot.config.bot.delete:
    await ctx.message.delete()
  bot.refresh()
  
  # send confirmation
  await ctx.send(
    'reloaded', 
    delete_after=bot.config.embeds.delete_after
  )

# -- start running the bot -- #
bot.go()
