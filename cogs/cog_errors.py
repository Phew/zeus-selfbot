''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import logging
import traceback

# -- 3rd party libararies -- #
from discord.ext import commands
from discord.ext.commands import errors
import discord

class Errors(commands.Cog):
  '''cog for handling errors'''
  def __init__(self, bot):
    logging.info('Loaded Errors Cog')
    self.ignored = (
      errors.MissingRequiredArgument,
      errors.TooManyArguments,
      errors.BadArgument,
      errors.CommandNotFound
    )
    self.config = bot.config
    self.embeds = bot.embeds
    self.bot = bot
    
  def in_ignored(self, e):
    return isinstance(e, self.ignored)

  # @commands.Cog.listener()
  # async def on_command_error(self, ctx, error):
  #   print(f'CTX: {ctx}')

  #   print(f'ERROR: {error}')
    
  #   if self.in_ignored(error):
  #     logging.info('Error Occured But Was Ignored')
  #     return

  #   logging.error(traceback.format_exc())
  #   print('An Error Occured Check The Log File')

# -- load the cog -- #
def setup(bot):
  bot.add_cog(Errors(bot))
