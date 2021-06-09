import discordBotModules
import utilityFunctions

try:
	import discord
	import praw
	import tqdm

except ModuleNotFoundError: #user has not installed required dependencies
	discordBotModules.botUtilityFunctions().installDependencies(['discord', 'praw', 'tqdm'])

prefix = '.'
client = discord.Client()
botUtility = utilityFunctions.botUtilityFunctions()
JSONContent = botUtility.retrieveJSONContent()
reddit = praw.Reddit(
	client_id = JSONContent["client_id"],
	client_secret = JSONContent["client_secret"],
	user_agent = JSONContent["user_agent"],
	username = JSONContent["username"],
	password = JSONContent["password"])

botFunctions = discordBotModules.discordBotFunctions(reddit, discord)
botFunctions.startup()

@client.event
async def on_ready():
    print(f'Joined as {client.user}')

@client.event
async def on_message(msg):
	try:
		if msg.author ==  client.user: #no infinite loops
			return

		if msg.content.startswith(prefix + 'help'): #.help on discord
			await msg.channel.send(botFunctions.help())

		elif msg.content.startswith(prefix + 'greet'): #.greet on discord
			await msg.channel.send(msg.author.mention + botFunctions.greet())

		elif msg.content.startswith(prefix + 'search'): #.search {query} on discord
			
			query = msg.content[8:]
			await msg.channel.send(f'Finding ten URLS with the search query `{query}`')
			
			returnedResults = botFunctions.search(query)
			await msg.channel.send(returnedResults[0])
			await msg.channel.send(returnedResults[1])

		elif msg.content.startswith(prefix + 'reddit'): #.reddit on discord
			embed = botFunctions.reddit()
			await msg.channel.send(embed=embed)

		elif msg.content.startswith(prefix + 'util'): #.util on discord
			await msg.channel.send(botFunctions.util())

		elif msg.content.startswith("stfu" or "shut up"): #just type "stfu" or "shut up" on discord
			await msg.channel.send(f"{msg.author.mention} https://tenor.com/view/stfu-no-one-cares-gif-21262364")

	except KeyboardInterrupt:
		threads = botFunctions.threads #get all timer objects
		for thread in threads:
			thread.join() #join all timer object threads, idk if you actually have to do this
		sys.exit()

	except discord.DiscordException as e:
		await msg.author.send(botUtility.errorOccured(msg.author, e)) #prints error message and sends one to the user that caused the error

client.run(JSONContent["token"])
