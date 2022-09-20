import discord
from discord.ext import commands
import asyncio
from webserver import keep_alive
import os
import random
import aiohttp
import json
from discord import Client, Intents, Embed
from discord import Client, Intents, Embed
import datetime
from datetime import time

with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

with open("users.json", "ab+") as ab:
    ab.close()
    f = open('users.json','r+')
    f.readline()
    if os.stat("users.json").st_size == 0:
      f.write("{}")
      f.close()
    else:
      pass
 
with open('users.json', 'r') as f:
  users = json.load(f)

intents=discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=["SG!","sg!","sG!","Sg!"],activity=discord.Activity(type=discord.ActivityType.watching, name="SG Network"),status=discord.Status.idle, intents = intents)

bot.remove_command('help')

@bot.command()
async def help(ctx, r=None):
 if r is None:
  embed = discord.Embed(title="", color=0xf5f5f5)
  embed.add_field(name="Moderation", value="`SG!help moderation`", inline=False)
  embed.set_thumbnail(url=str(bot.user.avatar.url))
  embed.add_field(name="Support", value="`SG!help support`") 
  embed.add_field(name="Ticket", value="`SG!help ticket`", inline=False)
  embed.add_field(name="Giveaway", value="`SG!help giveaway`", inline=False)
  embed.add_field(name="Fun", value="`SG!help fun`", inline=False)
  embed.set_author(name="Command List",icon_url=str(bot.user.avatar.url))
  await ctx.send(embed=embed)

 elif r == 'moderation':
  embed = discord.Embed(title="", color=0xf5f5f5)
  embed.add_field(name="Purge", value="`SG!Purge <amount>`", inline=False)
  embed.add_field(name="Mute", value="`SG!mute <User> <reason>`", inline=False)
  embed.add_field(name="Unmute", value="`SG!unmute <User>`", inline=False)
  embed.add_field(name="Kick", value="`SG!kick <User> <reason>`", inline=False)
  embed.add_field(name="Ban", value="`SG!ban <User> <reason>`", inline=False)
  embed.add_field(name="Unban", value="`SG!unban <User>`", inline=False)
  embed.add_field(name="Warn", value="`SG!Warn <user> <reason>`", inline=False)
  embed.set_author(name='Moderation',        icon_url=str(bot.user.avatar.url))
  embed.set_thumbnail(url=str(bot.user.avatar.url))
  await ctx.send(embed=embed)
  
 elif r == 'support':
  embed = discord.Embed(title="", color=0xf5f5f5)
  embed.add_field(name="Say", value="`SG!say <MSG>`", inline=False)
  embed.add_field(name="Poll", value="`SG!poll <option 1> <option 2> <question>`", inline=False)
  embed.add_field(name="suggest", value="`S!suggest <suggestion>`", inline=False)
  embed.add_field(name="Warns", value="`SG!warns <User>`", inline=False)
  embed.add_field(name="Embed", value="`SG!Embed <Title> <Body>`", inline=False)
  embed.set_author(name='Support',icon_url=str(bot.user.avatar_url))
  embed.set_thumbnail(url=str(bot.user.avatar_url))
  await ctx.send(embed=embed)	 

 elif r == 'fun':
  embed = discord.Embed(title="", color=0xf5f5f5)
  embed.add_field(name="Avtar", value="`SG!av <user>`", inline=False)
  embed.add_field(name="Rank", value="`SG!rank <user>`", inline=False)
  embed.add_field(name="Roll", value="`SG!roll <No. limit>`", inline=False)
  embed.set_author(name='Fun',icon_url=str(bot.user.avatar.url))
  embed.set_thumbnail(url=str(bot.user.avatar.url))
  await ctx.send(embed=embed)
 elif r == 'ticket':
  embed = discord.Embed(title="", color=0xf5f5f5)
  embed.add_field(name="Create", value="`SG!ticket create`", inline=False)
  embed.add_field(name="Close", value="`SG!ticket close`", inline=False)
  embed.set_author(name='Ticket',icon_url=str(bot.user.avatar.url))
  embed.set_thumbnail(url=str(bot.user.avatar.url))
  await ctx.send(embed=embed) 
 elif r == 'giveaway':
  embed = discord.Embed(title="", color=0x00f9ff)
  embed.add_field(name="Giveaway", value="`SG!giveaway <Time in Second> <Price>`", inline=False)
  embed.add_field(name="Reroll", value="`SG!reroll <ID of giveaway msg>`", inline=False)
  embed.set_author(name='Fun',icon_url=str(bot.user.avatar.url))
  embed.set_thumbnail(url=str(bot.user.avatar.url))
  await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)

async def purge(ctx, amount=1000):
   await ctx.message.delete()
   await ctx.channel.purge(limit=amount)
   await ctx.send('**successfully deleted messages**')

@bot.command()
@commands.has_permissions(ban_members=True)

async def ban(ctx, member: discord.Member, *, reason=None):

   await member.ban(reason=reason)

   await ctx.send(f'**User** {member} **has been ban**')


@bot.command()
@commands.has_permissions(kick_members=True)

async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

    await ctx.send(f'**User ** {member} **has been kick**')


@bot.command()
@commands.has_permissions(ban_members=True)

async def unban(ctx, *, member):
      banned_users = await ctx.guild.bans()

      member_name, member_discriminator = member.split('#')
      for ban_entry in banned_users:
         user = ban_entry.user

         if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"**Unbanned**: {user}")

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            await ctx.send("**Created Mute role pls use again to Mute**")
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False,send_messages=False, read_messages=True)

                return

        if mutedRole:
                await member.add_roles(mutedRole)
                await member.send(f"**you have been muted from: {guild.name} reason: {reason}**")
                await ctx.send(f"**member has been muted for** {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await ctx.send(f"**member has been unmuted**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
        await ctx.message.delete()
        await ctx.send(f"{message}")
        print(f"{ctx.author} Said '{message}'") 

@bot.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx, option1=None,option2=None, *, question):
    await ctx.message.delete()
    newline = '\n'
    string = f"str1{newline}str2"
    L = f'''1️⃣ {option1} {newline} {newline}2️⃣ {option2}'''
    embed = discord.Embed(title=f'{question}' ,color=0xf5f5f5, description=f'{L}')
    embed.set_thumbnail(url=str(bot.user.avatar.url))
    embed.set_footer(text=f'Poll By {ctx.author.name}', icon_url=ctx.author.avatar.url)
    message = await ctx.send(embed=embed)
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')
    
@bot.command()
async def suggest(ctx, *, S = None):
  await ctx.message.delete()
  channel = discord.utils.get(ctx.guild.text_channels, name = '👏・ꜱᴜɢɢᴇꜱᴛɪᴏɴs')
  if S is None:
   await ctx.send("**Pls Give your suggestion**")
  else:
    embed = discord.Embed(title='Suggestion' ,color=0xf5f5f5 , description=f'{S}')
    embed.set_thumbnail(url=str(bot.user.avatar.url))
    embed.set_footer(text=f'By {ctx.author.name}', icon_url=ctx.author.avatar.url)
    
    message = await channel.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('❎')

@bot.command() 
@commands.has_permissions(manage_roles=True)

async def warn(ctx ,user:discord.User , *,reason=None):
  guild = ctx.guild
  if reason is None:
    await ctx.send("**Please provide a reason**")
    return
  reason = ''.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.id:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.id,
      'reasons': [reason]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)
    
    await asyncio.sleep(2)
    await ctx.send(f"**member has been Warn for** {reason}")
    await asyncio.sleep(2)
    await user.send(f"**you have been Warn from: {guild.name} reason: {reason}**")

@bot.command(pass_context = True) 
@commands.has_permissions(manage_roles=True)

async def warns(ctx, user:discord.User):
  await ctx.message.delete()
  for current_user in report['users']:
    if user.id == current_user['name']:

     embed = discord.Embed(title='Warns Report',color=0xf5f5f5, description=f'{user.name} has been Warned {len(current_user["reasons"])} times')
     embed.set_thumbnail(url=str(bot.user.avatar.url))
     await ctx.send(embed=embed)
     break
  else:
    await ctx.send(f"**{user.name} has never been reported**")

@bot.command(pass_context=True)
async def join(ctx):
  channel = ctx.author.voice.channel
  await channel.connect()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, T, *,B):
   embed = discord.Embed(title="", color=0xf5f5f5,  description=f'{B}')
   embed.set_thumbnail(url=str(bot.user.avatar.url))
   embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
   embed.set_author(name=f'{T}',
		                 icon_url=str(bot.user.avatar.url))
   await ctx.send(embed=embed)


@bot.command()
async def av(ctx, member: discord.Member=None):
  if member is None:
    embed = discord.Embed(title="", color=0xf5f5f5)
    embed.set_image(url=str(ctx.author.avatar.url))
    embed.set_author(name=f'{ctx.author.name} Avatar', icon_url=str(ctx.author.avatar.url))
    await ctx.send(embed=embed)

  else:
    embed = discord.Embed(title="", color=0xf5f5f5)
    embed.set_image(url=str(member.avatar.url))
    embed.set_author(name=f'{member.name} Avatar',icon_url=str(member.avatar.url))
    await ctx.send(embed=embed)
    

@bot.command()
async def ticket(ctx, r = None):
 if r is None:   
   await ctx.message.delete()

 elif r =='create':
   await ctx.message.delete()
   guild = ctx.guild
   author = ctx.author
   overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True)
}

   channel = await guild.create_text_channel(f'ticket-{ctx.author.name}', overwrites=overwrites)
   embed = discord.Embed(title=f'SG ticket', color=0xf5f5f5, description =f'{author.mention} Wait For <@&951750159354712094> To response And To close ticket tell a staff to use `SG!close ticket` to close Ticket')
   await channel.send(f'{author.mention} <@&951750159354712094>',embed=embed)
   await channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, attach_files=True, read_message_history=True, external_emojis=True)

 elif r == 'close': 
   guild = ctx.guild
   channel = discord.utils.get(ctx.guild.channels, name=f'ticket-{ctx.author.name}')
   await guild.delete_text_channel(f'ticket-{ctx.author.name}')

@bot.command(pass_context = True)
async def roll(ctx, N : int):
  if N is None:
    await ctx.send('**Pls Enter a Nummber**')
  else:
        R = random.randint(1,N)
        await ctx.send(f'**{R}**') 

@bot.command(pass_context = True)
async def membercount(ctx):
 embed = discord.Embed(title='Membercount', color=0xf5f5f5, description =f'There are currently **{ctx.guild.member_count}** members in the server!')

 await ctx.send(embed=embed)

@bot.command(pass_context = True)
async def fly(ctx):
  await ctx.send("Buttons!", components=[Button(label="Button", custom_id="button1")])
  res = await bot.wait_for("button_click") 
  
@bot.command()
async def sly(ctx):
    await ctx.send(
        "Selects!",
        components=[
            Select(
                placeholder="Select something!",
                options=[
                    SelectOption(label="a", value="a"),
                    SelectOption(label="b", value="b"),
                ],
                custom_id="select1",
            )
        ],
    )

    interaction = await bot.wait_for(
        "select_option", check=lambda inter: inter.custom_id == "select1"
    )
    await interaction.send(content=f"{interaction.values[0]} selected!")

@bot.command()
async def cd(ctx, T: int):
  if T is None:
    await ctx.send("**pls enter time**")
  else:
    M = await ctx.send("**Condown Started...**")
    await asyncio.sleep(T)
    await M.edit("**Condown Has Been End**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def giveaway(ctx, T: int, *, P=None): 
  embed = discord.Embed(title=f'{P}', color=0xf5f5f5, description =f'**Time Remaining　　　　　　　　　　　　　　{T} Seconds**',url="https://discord.gg/km57um2qBK")
  embed.set_footer(text=f"Hosted by {ctx.author.name}", icon_url=ctx.author.avatar.url)
  embed.set_image(url="https://cdn.discordapp.com/attachments/853553570964439071/925240032292384768/20211228_094310.jpg")
  msg = await ctx.send(embed=embed)
  await msg.add_reaction('🎉')
  await asyncio.sleep(T)
  new_msg = await ctx.channel.fetch_message(msg.id)
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))
  winner = random.choice(users)
  await msg.edit(f"**Congratulations! {winner.mention} you won `{P}`!**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def reroll(ctx, id_ : int):
  new_msg = await ctx.channel.fetch_message(id_)
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(bot.user))

  winner = random.choice(users)
  await msg.edit(f"**Congratulations! {winner.mention} you won `{P}`!**")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def close(ctx):
	 await ctx.message.channel.delete(reason='Ticket Closed')

@bot.event
async def on_member_join(member):
  arrow = bot.get_emoji(928494617786220584)
  fire = bot.get_emoji(923231178260115466)
  rgb = bot.get_emoji(927362568899678269)
  flowers = bot.get_emoji(933238009858502677)
  chack = bot.get_emoji(933238269108432956)
  thx = ":Thxx:"
  dil = bot.get_emoji(933248586303545354)
  newline = '\n'
  string = f"str1{newline}str2"
  W = f'''Hey {member.mention}, Welcome to **SG Network** {flowers}{newline}{newline}{rgb}**Make sure to Check** {chack}{newline}{arrow} <#951750182058483732> For Announcement {fire}{newline}{newline}{arrow} <#951750177495085056> For Server Rules {fire}{newline}{newline}{arrow} <#951750179218948116> For Role Informations {fire}{newline}{newline}{arrow} <#951750200060420106> For chating with others {fire}{newline}{newline}{arrow} <#951750185959174175> For wining Giveaways {fire}{newline}{newline}{thx}**Thx for joinig us** {dil}'''
  embed = discord.Embed(title="Welcome to SG Network!",color=0xf5f5f5,description=f"{W}",timestamp=datetime.datetime.utcnow())
  embed.set_footer(text =f"{member.name}  Joined", icon_url =str(member.avatar_url))
  embed.set_image(url="https://cdn.discordapp.com/attachments/894589498934046771/933568482241544192/standard_3.gif")
  embed.set_thumbnail(url=str(bot.user.avatar_url))
  await bot.get_channel(951750175284670466).send(f"{member.mention}",embed=embed)  

@bot.event
async def on_member_remove(member):
   await bot.get_channel(951750176559730759).send(f"{member} has left")

keep_alive()

TOKEN = os.environ.get("DISCORD_BOT_SECRET")
bot.run(TOKEN)