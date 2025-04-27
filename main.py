import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler= logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents= discord.Intents.default()
intents.message_content=True
intents.members=True

bot= commands.Bot(command_prefix='!',intents=intents)

secrets_role="help"

@bot.event
async def on_ready():
    print(f"We are ready {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send("Please refrain from using profanity.")
    if message.content.startswith('!hello'):
        await message.channel.send(f'Hello {message.author.name}!')

    await bot.process_commands(message)

@bot.command()
async def hello(ctx): #ctx -> context
    await ctx.send(f"Hello {ctx.author.mention}")
    
@bot.command()
async def assign(ctx):
    role=discord.utils.get(ctx.guild.roles,names=secrets_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"Role {role.name} has been assigned to you.")
    else:
        await ctx.send("Role not found.")
        
@bot.command()
async def remove(ctx):
    role=discord.utils.get(ctx.gild.roles,name=secrets_role)
    if role:
        await ctx.author.remove(role)
        await ctx.send(f"{ctx.author.mention} has had the {secrets_role} removed")
    else:
        await ctx.send("Role not found.")

@bot.command()
async def dm(ctx,*,msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message.")

@bot.command()
async def poll(ctx,*,question):
    embed=discord.Embed(title="New Poll",description=question)
    poll_message=await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
    

@bot.command()
@commands.has_role(secrets_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")


@secret.error
async def secret_error(ctx,error):
    if isinstance(error,commands.MissingRole):
        await ctx.send("You don't have the required role to access this command.")
        



bot.run(token, log_handler=handler,log_level=logging.DEBUG)
