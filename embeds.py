''' 
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import datetime

# -- 3rd party libararies -- #
import discord

class Embeds:
  def __init__(self, config):
    '''custom embeds class that each cog get's accsess to'''
    self.config = config.embeds
    self.url = self.config.link
    self.author = self.config.author
    self.author_url = self.config.author_url
    self.footer = self.config.footer
    self.footer_url = self.config.footer_url
    self.image_url = self.config.image_url
    self.color = self.config.color
    self.title = self.config.title
    self.description = self.config.description
    self.thumbnail = self.config.thumbnail

  def new_default_embed(self, title='', description='', 
  timestamp='', fields=()):
    '''function to create an embed using the defualt config'''
    
    # -- create a new embeds instance -- #s
    embed = discord.Embed(
      title=(title if title != '' else self.title),
      description=(description if description != '' else self.description),
      timestamp=(timestamp if timestamp != '' else datetime.datetime.now()),
      color=self.color,
      url=self.url
    )

    # -- set author -- #
    if self.author_url is not None:
      embed.set_author(name=self.author, icon_url=self.author_url)
    else:
      embed.set_author(name=self.author)

    # -- set footer -- #
    if self.footer_url is not None:
      embed.set_footer(text=self.footer, icon_url=self.footer_url) 
    else:
      embed.set_footer(text=self.footer)
    
    # -- set image -- #
    if self.image_url is not None:
      embed.set_image(url=self.image_url)
    
    # -- set thumbnail  -- #
    if self.thumbnail is not None:
      embed.set_thumbnail(url=self.thumbnail)

    # -- add fields -- #
    if len(fields) > 0:
      for f in fields:
        embed.add_field(name=f[0], value=f[1], inline=f[2])

    return embed

  def new_raw_embed(self, title='', description='', timestamp='', fields=(), 
    thumbnail=None, footer=None, footer_url=None, 
    author=None, author_url=None, url=None, image_url=None):
    '''function to create an embed from scratch'''

    # -- create a new embed instance and check if the values are not nil -- #
    embed = discord.Embed(
      title=(title if title != '' else self.title),
      description=(description if description != '' else self.description),
      timestamp=(timestamp if timestamp != '' else datetime.datetime.now()),
      color=self.color,
      url=(url if url is not None else self.url)
    )

    # -- set thumbnail -- #
    if thumbnail is None:
      if self.thumbnail is not None:
        embed.set_thumbnail(url=self.thumbnail)
    else:
      embed.set_thumbnail(url=thumbnail)
    
    # -- set image -- #
    if image_url is None:
      if self.image_url is not None:
        embed.set_image(url=self.image_url)
    else:
      embed.set_image(url=image_url)
    
    # -- set footer -- #
    if footer is None and footer_url is None:
      if self.footer_url is None:
        embed.set_footer(text=self.footer)
      else:
        embed.set_footer(text=self.footer, icon_url=self.footer_url)
    else:
      if footer_url is None:
        embed.set_footer(text=footer)
      else:
        embed.set_footer(text=footer, icon_url=footer_url)

    # -- set author -- #
    if author is None and author_url is None:
      if self.author_url is None:
        embed.set_author(name=self.author)
      else:
        embed.set_author(name=self.author, icon_url=self.author_url)
    else:
      if author_url is None:
        embed.set_author(name=author)
      else:
        embed.set_author(name=author, icon_url=self.author_url)
    
    # -- add the fields -- #
    if len(fields) > 0:
      for f in fields:
        embed.add_field(name=f[0], value=f[1], inline=f[2])
    
    return embed
