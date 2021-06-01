#a simple bot using the discord api
import discord
import random
import logging
import time
import googlesearch
import praw
import time
import os
import json
import tqdm
import threading

logging.basicConfig()
logging.getLogger('discord')
logging.getLogger('reddit')

client = discord.Client()
GreetList = ['Greetings!', 'Hello!', 'Hi!', 'Hey!']
version = '0.94'
prefix = '.'
embeds = []
current_meme = 0

path = os.path.normpath(__file__ + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'res')
os.makedirs(path, exist_ok=True)
file = path + os.sep + 'config.json'

threads = []

try:
    fetchedPosts = open(file, 'r')
except FileNotFoundError:
    fetchedPosts = open(file, 'w+')
char = fetchedPosts.read(1)
fetchedPosts.close()

with open(file, 'r') as config:
	data = []
	for line in config:
		data.append(json.loads(line))
	print(data)
	TOKEN = data[0]["token"]
	print("Our token is:" + TOKEN)
	CLIENT_ID = data[0]["client_id"]
	print("Our client id is:" + CLIENT_ID)
	CLIENT_SECRET = data[0]["client_secret"]
	print(CLIENT_SECRET)
	USER_AGENT = data[0]["user_agent"]
	print(USER_AGENT)
	USERNAME = data[0]["username"]
	print(USERNAME)
	PASSWORD = data[0]["password"]
	print(PASSWORD)
	config.close()

reddit = praw.Reddit(
	client_id = CLIENT_ID,
	client_secret = CLIENT_SECRET,
	user_agent = USER_AGENT,
	username = USERNAME,
	password = PASSWORD)
print(reddit.user.me())
print("successfully set up reddit")

def fetch(stop):
    print(f"Fetching new posts at {time.asctime()}.")
    subreddit = reddit.subreddit('memes')
    print("set subreddit to r/memes")
    hot_posts = list(subreddit.hot(limit=100))
    print(hot_posts)
    for posts in tqdm.tqdm(range(len(hot_posts)-1), desc = "Fetching posts..."):
        global current_meme
        current_meme = hot_posts[posts]
        if not current_meme.stickied and not current_meme.visited:
            embed = discord.Embed(
                title = current_meme.title,
                url = current_meme.url
            )
            embed.set_image(url = current_meme.url)
            embed.set_footer(text = f'{current_meme.score} ⬆️ | {len(current_meme.comments)} 💬')
            embeds.append(embed)

        else:
            hot_posts.remove(current_meme)
    current_meme = 0

    if not stop.is_set():
        # 28800 seconnds is 8 hours
        threads.append(threading.Timer(28800, fetch, [stop]).start())


stop = threading.Event()
start = time.time()
fetch(stop)
print("fetched all 100 posts.")
end = time.time()
print(f'Fetched all posts in {end-start} seconds.')

@client.event
async def on_ready():
    print(f'Joined as {client.user}')

@client.event
async def on_message(msg):
    try:
	    if msg.author ==  client.user:
	        return

	    if msg.content.startswith(prefix + 'help'):
	        print(f'{time.asctime()}: We received "{prefix}help" command!')
	        await msg.channel.send(f'''Commands for version `{version}`:
	        **{prefix}help** - sends this list of commands
	        **{prefix}greet** - says hello
	        **{prefix}search** - finds and retrieves ten urls based on your search query
	        **{prefix}reddit** - gets a meme from r/memes on Reddit''')

	    elif msg.content.startswith(prefix + 'greet'):
	        print(f'{time.asctime()}: We received the "{prefix}greet" command!')
	        await msg.channel.send(GreetList[random.randrange(0, 4, 1)])

	    elif msg.content.startswith(prefix + 'search'):
	        fetchedURLS = []
	        print(f'{time.asctime()}: We received the "{prefix}search" command!')
	        query = msg.content[8:]
	        await msg.channel.send(f'Finding ten URLS with the search query `{query}`')

	        for search_results in googlesearch.search(query, tld="com", num=10, stop=10, pause=2):
	            fetchedURLS.append(search_results)

	        await msg.channel.send(f'''Here are ten URLS based on your search `{query}`:''')
	        await msg.channel.send(fetchedURLS)

	    elif msg.content.startswith(prefix + 'reddit'):
	        global current_meme
	        try:
	            await msg.channel.send(embed=embeds[current_meme])
	            current_meme += 1

	        except IndexError:
	            current_meme = 0
	            await msg.channel.send("out of memes lol")

    except KeyboardInterrupt:
        for thread in threads:
            thread.join()
        sys.exit()

    except Exception as e:
        print("something happened uh oh stinky poopoo" + e)
        await msg.channel.send("something happened uh oh stinky poopoo" + e)

client.run(TOKEN)
