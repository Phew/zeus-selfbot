''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import socket
import logging

# -- 3rd party libararies -- #
from discord.ext import commands
import discord
import ipapi
import pythonping

class Network(commands.Cog):
  '''A cog for handling commands related to networking'''
  def __init__(self, bot):
    logging.info('Network Cog Loaded')
    self.config = bot.config
    self.embeds = bot.embeds
    self.bot = bot
    
  @commands.command(name='getip')
  async def host_to_ip(self, ctx, *, host: str):
    ip = socket.gethostbyname(host)
    embed = self.embeds.new_default_embed(
      title='**IP Found**',
      description='Host To IP Lookup Successfull',
      fields=(
        ('Host', host, False),
        ('IP', ip, True)
      )
    )
    await ctx.send(
      embed=embed,
      delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()

  @commands.command(name='gethost')
  async def ip_to_host(self, ctx, *, ip: str):
    # -- attempt to get the ip and create and embed -- #
    host = socket.gethostbyaddr(ip)
    embed = self.embeds.new_default_embed(
      title='**Host Found**',
      description='IP To Host Lookup Successfull',
      fields=(
        ('IP', ip, False),
        ('Host', host[0], True)
      )
    )
    await ctx.send(
      embed=embed,
      delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()

  @commands.command(name='iplookup')
  async def ip_lookup(self, ctx, *, ip: str):
    ip_info = ipapi.location(ip=ip)
    embed = self.embeds.new_default_embed(
      title='**IP Info Found**',
      description=f'Found Info For: {ip}',
      fields=(
        ('IP', ip, False),
        ('Country', ip_info['country_name'], True),
        ('Region', ip_info['region'], True),
        ('City', ip_info['city'], True),
        ('Asn', ip_info['asn'], True),
        ('Org', ip_info['org'], True)
      )
    )
    await ctx.send(
      embed=embed,
      delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()

  @commands.command(name='ping')
  async def is_live(self, ctx, *, ip: str):
    result = pythonping.ping(ip, verbose=False)
    await ctx.send(
      embed=self.embeds.new_default_embed(
        title='Ping Results', 
        description=f'Returning Ping Results For: {ip}',
        fields=(
          ('Is Live', result.success(), False),
          ('Output', '```%s```' % "\n".join(str(x) for x in result), True)
        )
      ), 
      delete_after=self.config.embeds.delete_after
    )    
    if self.config.bot.delete:
      await ctx.message.delete()

# -- load the cog -- #
def setup(bot):
  bot.add_cog(Network(bot))
