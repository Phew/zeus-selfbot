''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libaries -- #
import logging
import asyncio

# -- 3rd party libararies -- #
import discord
from discord.ext import commands
import requests

# -- local libraries -- #
import cogs.utils.util_checks as checks

class Messaging(commands.Cog):
  link = 'https://discordapp.com/api/v6/entitlements/gift-codes/'
  def __init__(self, bot):
    logging.info('Messages Cog Loaded')
    self.copy = []
    self.config = bot.config
    self.embeds = bot.embeds
    self.bot = bot
  
  @commands.command(name='type')
  async def fake_type(self, ctx, amount: int):
    if self.config.bot.delete:
      await ctx.message.delete()
    async with ctx.typing():
      await asyncio.sleep(amount)

  @commands.command(name='purge')
  async def purge_ctx(self, ctx, amount=None):
    if self.config.bot.delete:
      await ctx.message.delete()
  
    i = 0
    async for message in ctx.channel.history(limit=amount):
      if message.author == self.bot.user and not message.is_system():
        await message.delete()
        i += 1
   
    await ctx.send(
      embed=self.embeds.new_default_embed(
        title='Cleared Messages In Current Chat',
        description='Amount: %d' % i
      ), 
      delete_after=self.config.embeds.delete_after
    )
  
  @commands.command(name='purgefilter')
  async def purge_ctx_by_filter(self, ctx, word: str, amount=None):
    if self.config.bot.delete:
      await ctx.message.delete()
  
    i = 0
    async for message in ctx.channel.history(limit=amount):
      if (
        message.author == self.bot.user 
        and not message.is_system() 
        and word.casefold() in \
          message.content.casefold()
      ):
        await message.delete()
        i += 1
   
    await ctx.send(
      embed=self.embeds.new_default_embed(
        title='Cleared Messages In Current Chat',
        description='Amount: %d, Filter: %s' % (
          i, word
        )
      ), 
      delete_after=self.config.embeds.delete_after
    )
    
  @commands.command(name='dmpurge') 
  async def purge_dms(self, ctx, amount=None):
    if self.config.bot.delete:
      await ctx.message.delete()
    
    i = 0
    for channel in self.bot.private_channels:
      async for message in channel.history(limit=None):
        if message.author == self.bot.user and not message.is_system():
          await message.delete()
          i += 1

    await ctx.send(
      embed=self.embeds.new_default_embed(
        title='Cleared Messages In Every Server',
        description='Amount: %d' % i
      ), 
      delete_after=self.config.embeds.delete_after
    )
    
  @commands.command(name='channelpurge')
  async def purge_channels(self, ctx):
    if self.config.bot.delete:
      await ctx.message.delete()
    
    i = 0
    async for channel in self.bot.get_all_channels():
      async for message in channel.history(limit=None):
        if message.author == self.bot.user and not message.is_system():
          await message.delete()
          i += 1
    
    await ctx.send(
      embed=self.embeds.new_default_embed(
        title='Cleared Messages In Every Server',
        description='Amount: %d' % i
      ), 
      delete_after=self.config.embeds.delete_after
    )

  @commands.command(name='spam')
  async def spam_ctx(self, ctx, amount: int, *, message: str):
    if self.config.bot.delete:
      await ctx.message.delete()
    for _ in range(amount):
      await ctx.send(
       message
      )
  
  @commands.command(name='spamembed')
  async def spam_ctx_embed(self, ctx, amount: int, *, message: str):
    if self.config.bot.delete:
      await ctx.message.delete()
    for _ in range(amount):
      await ctx.send(
        embed=self.embeds.new_default_embed(
          title=message
        )
      )
    
  @commands.command(name='stopcopy')
  async def stop_copy_user(self, ctx, user: str):
    if (user := checks.get_user(user, ctx, self.bot)) is None and user != ctx.author:
      if self.config.bot.delete:
        await ctx.message.delete()
      return

    if user.id not in self.copy:
      if self.config.bot.delete:
        await ctx.message.delete()
      return
    self.copy.remove(user.id)
    if self.config.bot.delete:
      await ctx.message.delete()

    await ctx.send(
      embed=self.embeds.new_default_embed(
        title=f'Stopped Copying User',
        description=f'Stopped Copying {user.mention}'
      ),
      delete_after=self.config.embeds.delete_after
    )

  @commands.command(name='startcopy')
  async def copy_user(self, ctx, user: str):
    if (user := checks.get_user(user, ctx, self.bot)) is None and user != ctx.author:
      if self.config['bot'].delete:
        await ctx.message.delete()
      return

    if user in self.copy:
      if self.config.bot.delete:
        await ctx.message.delete()
      return
    self.copy.append(user.id) 
    if self.config.bot.delete:
      await ctx.message.delete()

    await ctx.send(
      embed=self.embeds.new_default_embed(
        title=f'Copying User',
        description=f'Now Copying {user.mention}'
      ),
      delete_after=self.config.embeds.delete_after
    )
  
  @commands.Cog.listener()
  async def on_message(self, ctx):
    # -- copying -- #
    if ctx.author.id in self.copy and ctx.content:
      await ctx.channel.send(ctx.content)
      return

    # -- get nitro -- #
    if self.config.bot.sniper:
      if (code := checks.is_nitro(ctx.content)):
        result = requests.post(
          Messaging.link + code + '/redeem',
          json={'channel_id': str(ctx.channel.id)},
          headers={'authorization': self.config.bot.token, 'user-agent': 'Mozilla/5.0'},
        )
        claimed = str(result.content)

        if 'This gift has been redeemed already' in claimed:
          await ctx.channel.send(
            embed=self.embeds.new_default_embed(
              title=f'**Error**',
              description=f'Could Not Claim Nitro: {code}, Already Claimed'
            ),
            delete_after=self.config.embeds.delete_after
          )
          return
        
        if 'Unknown Gift Code' in claimed:
          await ctx.channel.send(
            embed=self.embeds.new_default_embed(
              title=f'**Error**',
              description=f'Could Not Claim Nitro: {code}, Invalid Code'
            ),
            delete_after=self.config.embeds.delete_after
          )
          return

        if 'nitro' in claimed:
          await ctx.channel.send(
            embed=self.embeds.new_default_embed(
              title=f'**Claimed Nitro**',
              description=f'Successfully Claimed Nitro: {code}'
            ),
            delete_after=self.config.embeds.delete_after
          )
          return

    if self.config.bot.log: 
      data = checks.get_data()
      if (
        (ctx.author.id in self.config.log.user_ids) or
        ((x:=ctx.guild) is not None and x.id in self.config.log.guild_ids)
        or (any(k in ctx.content for k in self.config.log.keywords))
      ):
        data['author']['name'] = f'{ctx.author.name}#{ctx.author.discriminator}'
        data['author']['id'] = ctx.author.id
        data['message']['time'] = str(ctx.created_at)
        data['message']['content'] = ctx.content if ctx.content else 'No Content'
        data['message']['id'] = ctx.id
        data['message']['nonce'] = ctx.nonce
        data['server']['id'] = ctx.guild.id if ctx.guild is not None else 'Dm or Group'
        data['server']['name'] = ctx.guild.name if ctx.guild is not None else 'Dm or Group'
        self.bot.new_log(data)
    
# -- load the cog -- #
def setup(bot):
  bot.add_cog(Messaging(bot))
