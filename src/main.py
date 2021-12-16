# This code was made by moistpotato9873 on GitHub!
# Check out the original code at https://github.com/moistpotato9873/moistpotatos-bot
# The modified code's repository can be found at [your repo link]
import sys
import utilityFunctions # utilityFunctions has no dependencies so we can import that first
import discordBotModules # if google is not installed, installDependencies will be called there
import workFunctions
import os

try:
	import discord
	from discord.ext import commands
	from discord.ext.commands.errors import CommandNotFound
	
#	import praw

except ImportError as e: # one of the modules above hasn't been installed
	print(str(e))
	utilityFunctions.botUtilityFunctions().installDependencies(['discord'])

#import praw # if it's not imported again it throws a NameError

#botUtility = utilityFunctions.botUtilityFunctions()
#work = workFunctions.work()

#JSONContent = botUtility.retrieveJSONContent(key="bot_info")
client = commands.Bot(
	command_prefix=".", 
	help_command=None)
#	owner_id=JSONContent["owner_id"]
#reddit = praw.Reddit(
#	client_id = JSONContent["client_id"],
#	client_secret = JSONContent["client_secret"],
#	user_agent = JSONContent["user_agent"],
#	username = JSONContent["username"],
#	password = JSONContent["password"])

#botFunctions = discordBotModules.discordBotFunctions(reddit, discord) # pass in our reddit and discord objects in order to use discordBotModules' methods
#botFunctions.startup() # like this one

@client.event
async def on_ready():
    print(f'Joined as {client.user}')

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		return
	await ctx.author.send(botUtility.errorOccured(ctx.author, error))

@client.command()
async def help(ctx):
	await ctx.channel.send(embed=botFunctions.help(ctx.author.name, ctx.author.avatar_url))

@client.command()
async def greet(ctx):
	await ctx.channel.send(f"{ctx.author.mention} {botFunctions.greet()}")

@client.command()
async def search(ctx, *args):
	query = ""

	for arg in args:
		query += " " + arg

	query = query[1:]

	if query == "":
		await ctx.channel.send("need a query")

	else:
		msg = await ctx.channel.send(f'Finding ten URLS with the search query `{query}`')
		returnedResults = await botFunctions.search(query, JSONContent["user_agent"], msg)
		await msg.edit(content="Organizing results..")
		urls = returnedResults[0]
		titles = returnedResults[1]
		embed = discord.Embed(title=f"Returned results for `{query}`")
		for i in range(len(urls)):
			embed.add_field(name=titles[i], value=urls[i], inline=False)
		
		await msg.edit(content="Done!")
		await ctx.channel.send(embed=embed)

#@client.command(name="reddit", aliases=["rdt"])
#async def _reddit(ctx):
#	embed = botFunctions.reddit()
#	await ctx.channel.send(embed=embed)

@client.command(name="ping")
async def _ping(ctx):
	ping = client.latency * 1000
	await ctx.channel.send(f":ping_pong: Pong! **{round(ping)}ms**")

#@client.command(name="work")
#async def _work(ctx):
#	authorID = str(ctx.author.id)
#	if not work.work(authorID):
#		await ctx.channel.send(f"heyheyhey what r u doing u need a job, choose a job from this list using `.workas`:\n{work.jobList}")
#
#	else:
#		await ctx.channel.send(work.work(authorID))
#
#@client.command(name="workas")
#async def _workas(ctx, *args):
#	job = ""
#	authorID = str(ctx.author.id)
#
#	for word in args:
#		job += " " + word
#	
#	job = job[1:]
#
#	if not work.workas(job):
#		await ctx.channel.send(f"uh so {job} isn't a valid job, choose one from this list: {work.jobList}")
#
#	else:
#		await ctx.channel.send(f"nice ur working as a(n) {job}")
#		user = work.query(authorID, query="work_info")
#		if user:
#			user["job"] = job
#			botUtility.dumpToJSON(authorID, newWorkData=user)
#		else:
#			botUtility.dumpToJSON(authorID)
#			user = work.query(authorID, query="work_info")
#			user["job"] = job
#			botUtility.dumpToJSON(authorID, newWorkData=user)
#	
#@client.command(name="bal", aliases=["balance"])
#async def _bal(ctx):
#	moneyInfo = work.query(str(ctx.author.id), query="money_info")
#	wallet = moneyInfo["wallet"]
#	bank = moneyInfo["bank"]
#	bankSpace = moneyInfo["bankSpace"]
#	bankPercentage = bank / bankSpace
#	embed = discord.Embed(title = f"{ctx.author.name}'s balance")
#	embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
#	embed.add_field(name="Wallet", value=f"{wallet} coins", inline=False)
#	embed.add_field(name="Bank", value=f"{bank}/{bankSpace} coins ({bankPercentage*100}%)", inline=False)
#	embed.set_footer(text="shop coming soon")
#	await ctx.channel.send(embed=embed)
#
#@client.command(name="dep", aliases=["deposit"])
#async def _dep(ctx, amount=None):
#	moneyInfo=work.query(str(ctx.author.id), query="money_info")
#	bankSpace = moneyInfo["bankSpace"]
#	wallet = moneyInfo["wallet"]
#	if wallet == 0:
#		await ctx.channel.send("**listen. you are broke. stop putting 0 coins into the bank.**")
#
#	else:
#		try:
#			if amount and amount != "all":
#				amount = float(amount)
#				amount = int(amount)
#				moneyInfo["wallet"] -= amount
#				moneyInfo["bank"] += amount
#				
#				if moneyInfo["bank"] > bankSpace:
#					await ctx.channel.send("u literally cannot fit any more money into ur bank my guy")
#					moneyInfo["bank"] -= amount
#					moneyInfo["wallet"] += amount
#
#				else:
#					botUtility.dumpToJSON(str(ctx.author.id), newMoneyData=moneyInfo)
#					await ctx.channel.send(f"`{amount}` coins deposited into your bank.")
#
#			elif amount == "all":
#				moneyInfo["bank"] += wallet
#				moneyInfo["wallet"] -= wallet
#				
#				if moneyInfo["bank"] > bankSpace:
#					difference = moneyInfo["bank"] - bankSpace
#					moneyInfo["wallet"] += difference
#					moneyInfo["bank"] -= difference
#					botUtility.dumpToJSON(str(ctx.author.id), newMoneyData=moneyInfo)
#					await ctx.channel.send(f"All coins deposited into your bank. `{difference}` coins are left in your wallet since it exeeded your bank space.")
#
#				else:
#					botUtility.dumpToJSON(str(ctx.author.id), newMoneyData=moneyInfo)
#					await ctx.channel.send(f"`{wallet}` coins deposited into your bank.")
#			
#			else:
#				await ctx.channel.send("sooooooo u gotta deposit some money, i can't just put nothing in the bank")
#
#		except ValueError:
#			await ctx.channel.send(f"`{amount}` isn't a valid number dummy")
#
@client.command(name="exit")
async def _exitProgram(ctx):
	await ctx.author.send("enter the file location for the bot to confirm")
	print("someone is trying to shutdown the bot")
	print(__file__)

@client.command(name="util")
async def _util(ctx):
	await ctx.channel.send(botFunctions.util())

@client.event
async def on_message(msg):
	try:
		if msg.author == client.user:
			return

#		author = str(msg.author.id)
#		lastWorkCmd = work.query(author, query="work_info")

#		if not lastWorkCmd: # check if query returned False
#			lastWorkCmd = False

#		else:
#			lastWorkCmd = lastWorkCmd["lastWorkCmd"]

		if "stfu" in msg.content or "shut up" in msg.content: # just type "stfu" on discord
			await msg.channel.send(f"{msg.author.mention} https://tenor.com/view/stfu-no-one-cares-gif-21262364")

		elif client.user.mentioned_in(msg):
			if "@everyone" in msg.content or "@here" in msg.content:
				return
			await msg.channel.send(f"{msg.author.mention} TF R U DOING PINGING A BOT https://tenor.com/view/bronwie-shut-up-bronwie-gif-19682564")

		elif msg.content == __file__ and not msg.guild:
			await msg.channel.send("bot shutting down...")
			print(f"{msg.author} shut down the bot")
			sys.exit()

#		elif lastWorkCmd == True:
#			workStr = msg.content.lower()
#			await msg.channel.send(work.checkCP(str(msg.author.id), workStr))

		await client.process_commands(msg)

	except discord.DiscordException as e:
		await msg.author.send(botUtility.errorOccured(msg.author, e)) # prints error message and sends one to the user that caused the error

path = os.path.normpath(__file__ + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'res')
os.makedirs(path, exist_ok=True)
file = path + os.sep + 'token.txt'
with open(file) as f:
    client.run(f.read())
