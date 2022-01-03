import sys
import os
import random

import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

client = commands.Bot(command_prefix=".", help_command=None)
greetList = ['Greetings!', 'Hello!', 'Hi!', 'Hey!']

@client.event
async def on_ready():
    print(f'Joined as {client.user}')

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		return
	await ctx.channel.send(f":skull: `{error}` :skull:")

@client.command()
async def help(ctx):
	await ctx.channel.send("this is a help function")

@client.command()
async def greet(ctx):
	await ctx.channel.send(f"{ctx.author.mention} {greetList[random.randrange(0, 4, 1)]}")

@client.command(name="ping")
async def _ping(ctx):
	ping = client.latency * 1000
	await ctx.channel.send(f":ping_pong: Pong! **{round(ping)}ms**")

@client.command(name="exit")
async def _exitProgram(ctx):
	await ctx.author.send("enter the file location for the bot to confirm")
	print("someone is trying to shutdown the bot")
	print(__file__)

@client.command(name="util")
async def _util(ctx):
	await ctx.channel.send(f"running on {os.system('whoami')}")

@client.event
async def on_message(msg):
	try:
		if msg.author == client.user:
			return

		if "stfu" in msg.content or "shut up" in msg.content: # just type "stfu" on discord
			await msg.channel.send(f"{msg.author.mention} https://tenor.com/view/stfu-no-one-cares-gif-21262364")

		elif client.user.mentioned_in(msg):
			await msg.channel.send(f"{msg.author.mention} https://tenor.com/view/bronwie-shut-up-bronwie-gif-19682564")

		elif msg.content == __file__ and not msg.guild:
			await msg.channel.send("bot shutting down...")
			print(f"{msg.author} shut down the bot")
			sys.exit()

		await client.process_commands(msg)

	except discord.DiscordException as error:
		await msg.channel.send(f":skull: `{error}` :skull:") # prints error message and sends one to the user that caused the error


with open('token.txt') as f:
    client.run(f.read())
