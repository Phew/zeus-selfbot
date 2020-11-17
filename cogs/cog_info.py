''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import logging

# -- 3rd party libararies -- #
import discord
from discord.ext import commands

# -- local libraries -- #
import cogs.utils.util_checks as checks

class Info(commands.Cog):
  '''A cog for handling commands related to user and server info'''
  def __init__(self, bot):
    logging.info('Info Cog Loaded')
    self.config = bot.config
    self.embeds = bot.embeds
    self.bot = bot
  
  @commands.command(name='uav')
  @commands.has_permissions(embed_links=True)
  async def get_av(self, ctx, name: str):
    if (user := checks.get_user(name, ctx, self.bot)) is None:
      if self.config.bot.delete:
        await ctx.message.delete()
      return

    await ctx.send(
      embed=self.embeds.new_raw_embed(
        title='**Found profile picture**',
        description=f'Showing profile picture for: {user.mention}',
        image_url=user.avatar_url
      ), 
      delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()
  
  @commands.command(name='userinfo')
  @commands.has_permissions(embed_links=True)
  async def get_info(self, ctx, name: str):
    if (user := checks.get_user(name, ctx, self.bot)) is None:
      if self.config.bot.delete:
        await ctx.message.delete()
      return

    embed = self.embeds.new_raw_embed(
      title='**User Info Found**',
      description=f'Found Info For: {user.mention}',
      fields=(
        
        ('ID', user.id, True),
        
        # nickname
        (
          ('Nick', user.nick, True) 
          if checks.is_mem(user) else 
          ('Nick', 'Only Avaible In Server', True)
        ),
        
        # status
        (
          ('Status', user.status, True) 
          if checks.is_mem(user) else 
          ('Status', 'Only Avaible In Server', True)
        ),
        
        # voice
        (
          ('Voice', None if not user.voice else user.voice.channel, True) 
          if checks.is_mem(user) else 
          ('Voice', 'Only Avaible In Server', True)
        ), 
        
        # game
        (
          ('Game', user.activity, True) 
          if checks.is_mem(user) else 
          ('Game', 'Only Avaible In Server', True)
        ),
        
        # role
        (
          ('Role', user.top_role.name, True) 
          if checks.is_mem(user) else
          ('Role', 'Only Avaible In Server', True)
        ),
        
        # created 
        ('Created', user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), False),
        
        # joined server
        (
          ('Joined', user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), False) 
          if checks.is_mem(user) else 
          ('Joined', 'Only Avaible In Server', True)
        )
      
      ), 
      thumbnail=user.avatar_url
    )

    await ctx.send(
      embed=embed, 
      delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()

  @commands.command(name='serverinfo')
  @commands.has_permissions(embed_links=True)
  async def get_server_info(self, ctx):
    '''returns info about the specified server'''
    if (
      isinstance(ctx.channel, discord.DMChannel) 
      or isinstance(ctx.channel, discord.GroupChannel) or 
      ctx.message.guild.unavailable
    ):
      if self.config.bot.delete:
        await ctx.message.delete()
      return

    server = ctx.message.guild

    # -- count online -- # 
    online = 0
    for user in server.members:
      if str(user.status) in ['online', 'idle', 'dnd']:
        online += 1

    # -- create all users string -- #
    users = []
    for user in server.members:
      users.append(f'{user.name}#{user.discriminator}')
    users.sort()
    all_users = '\n'.join(users)

    # -- get text channel count -- #
    text_channels = len([x for x in server.channels if type(x) == discord.channel.TextChannel])
    voice_channels = len([y for y in server.channels if type(y) != discord.channel.TextChannel])

    b = "\n".join([f'{m.name}#{m.discriminator}' for m in server.premium_subscribers])
    boosters = f'```{b}```' if b else 'No Boosters'

    # -- create an embed -- #
    embed = self.embeds.new_raw_embed(
      title='**Server Info Found**',
      description=f'Found Info For: {server.name}',
      fields=(
        ('Owner', server.owner, False),
        ('Name', server.name, True),
        ('ID', server.id, True),
        ('Members', server.member_count, True),
        ('Online', online, True),
        ('Text Channels', str(text_channels), True),
        ('Region', str(server.region), True),
        ('Verification', str(server.verification_level), True),
        ('Highest Role', server.roles[-1], True), 
        ('Default Role', str(server.default_role), True),
        ('Role Count', str(len(server.roles)), True),
        ('Emoji Count', str(len(server.emojis)), True),
        ('Created', server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), True),
        ('Boosters', boosters, False)
      ), thumbnail=server.icon_url
    )

    # -- send -- #
    await ctx.send(
      embed=embed, 
      delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()
      
  @commands.command(name='sav')
  @commands.has_permissions(embed_links=True)
  async def get_server_av(self, ctx):
    if (
      isinstance(ctx.channel, discord.DMChannel) 
      or isinstance(ctx.channel, discord.GroupChannel)
    ):
      if self.config.bot.delete:
        await ctx.message.delete()
      return
    server = ctx.message.guild

    await ctx.send(
      embed=self.embeds.new_raw_embed(
        title='Found Server Banner',
        description=f'Showing Banner For {server.name}',
        image_url=server.icon_url
      ), delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()

  @commands.command(name='sba')
  @commands.has_permissions(embed_links=True)
  async def get_server_banner(self, ctx):
    if (
      isinstance(ctx.channel, discord.DMChannel) 
      or isinstance(ctx.channel, discord.GroupChannel)
    ):
      if self.config.bot.delete:
        await ctx.message.delete()
      return
    server = ctx.message.guild
    
    await ctx.send(
      embed=self.embeds.new_raw_embed(
        title='Found Server Banner',
        description=f'Showing Banner For {server.name}',
        image_url=server.banner_url
      ), delete_after=self.config.embeds.delete_after
    )
    if self.config.bot.delete:
      await ctx.message.delete()

# -- load the cog -- #
def setup(bot):
  bot.add_cog(Info(bot))
