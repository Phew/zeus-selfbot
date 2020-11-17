''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import logging

# -- 3rd party libararies -- #
from discord.ext import commands
import discord

class Nuke(commands.Cog):
  def __init__(self, bot):
    logging.info('Loaded Nuke Commands Cog')
    self.config = bot.config
    self.embeds = bot.embeds
    self.bot = bot
  
  @commands.command(name='banall')
  @commands.bot_has_permissions(ban_members=True)
  async def ban_all(self, ctx):
    ignored = (
      ctx.message.channel.guild.me.id,
      ctx.message.channel.guild.owner_id
    )
    return


# -- load the cog -- #
def setup(bot):
  bot.add_cog(Nuke(bot))

    