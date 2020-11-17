'''
Author: k1rk and charge
Copyright: Zeus Selfbot (c) inc.
'''

# -- standard libraries -- #
import re

# -- 3rd party libraries -- #
import discord
from discord.ext import commands

re_code = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")

def is_mem(member):
  '''checks if a user is discord.Member'''
  return isinstance(member, discord.Member)

def get_user(user, context, bot):
  '''attempts to get user from a string'''
  if not user:
    return
  if len(context.message.mentions) == 0:
      if not is_mem(user):
        return
      user = context.guild.get_member_named(user)
  else:
    user = context.message.mentions[0]
  if not user:
    user = context.guild.get_member(int(user))
  if not user:
    user = bot.get_user(int(user))
  if user:
    return user

def is_nitro(content):
  '''check nitro is in a message content'''
  if (y := re_code.search(content)):
    c = y.group(2)
    if len(c) < 16:
      return False
    return c 
  return False

def is_group_or_dm(channel):
  '''returns true if channel is an instance of group or dm'''
  return (
    isinstance(channel, discord.DMChannel) 
    or isinstance(channel, discord.GroupChannel)
  )

def get_data():
  return {
      'author': {
        'name': None,
        'id': None
      },
    
      'message': {
        'time': None,
        'content': None,
        'id': None, 
        'nonce': None
      },

      'server': {
        'id': None,
        'name': None
      },
    }

