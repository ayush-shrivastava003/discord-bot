import time
import random
import threading
import socket
import requests
import utilityFunctions

try:
    import googlesearch
    from bs4 import BeautifulSoup
    import tqdm

except ImportError:
    print(f"Import Error at {__file__}")
    utilityFunctions.botUtilityFunctions().installDependencies(['bs4', 'google', 'tqdm'])

import tqdm
utilFuncs = utilityFunctions.botUtilityFunctions()

class discordBotFunctions():
    def __init__(self, reddit, discord):
        self.GreetList = ['Greetings!', 'Hello!', 'Hi!', 'Hey!']
        self.prefix = '.'
        self.version = '0.95'
        self.subreddits = ['memes', 'me_irl', 'dankmemes']
        self.embeds = []
        self.submissions = []
        self.post = None
        self.timeLastRefreshed = None
        self.threads = []
        self.redditObj = reddit
        self.discord = discord

    def fetch(self, stop):
        """
        Fetches new posts from Reddit. Reschedules using threading.Timer object.
        """
        self.timeLastRefreshed = time.asctime()
        print(f"Fetching new posts at {self.timeLastRefreshed}.")
        self.embeds = [] #clear any embeds from before

        print("Fetching submissions...")
        for i in tqdm.tqdm(range(len(self.subreddits)), desc="Fetching posts"):
            subreddit = self.subreddits[i]
            self.submissions.append(list(self.redditObj.subreddit(subreddit).hot(limit=100)))


        for i in range(len(self.subreddits)):
            print("Filtering submissions...")
            for posts in self.submissions[i]:
                if posts.stickied or "v.redd.it" in posts.url: #removing all pinned posts or non-gifs/images
                    self.submissions[i].remove(posts)

            print("Constructing embeds...")
            for posts in tqdm.tqdm(range(len(self.submissions[i])), desc = f"Constructing embeds for {self.subreddits[i]}"):
                self.post = self.submissions[i][posts]
                #creates embed to be used on discord
                embed = self.discord.Embed(
                    title = self.post.title,
                    url = f"https://reddit.com/{self.post.id}"
                )
                embed.set_image(url = self.post.url)
                embed.set_author(name=self.post.author.id, icon_url=self.post.author.icon_img)
                embed.set_footer(text = f'{self.post.score} ⬆️ | {len(self.post.comments)} 💬')
                self.embeds.append(embed)

            print(f"...done ({i+1}/{len(self.subreddits)})")

        self.post = 0


        if not stop.is_set():
            self.threads.append(threading.Timer(utilFuncs.getNextRefreshTime(), self.fetch, [stop]).start()) #set a timer for 8 hours to refresh the posts

    def help(self, authorName, authorPFP):
        """
        Returns a list of commands for the bot in the form of an embed.
        """
        embed = self.discord.Embed(title=f".help - all commands for version {self.version}", )
        embed.set_author(name=authorName, icon_url=authorPFP)
        embed.add_field(name=f"{self.prefix}help", value="sends this list of commands", inline=True)
        embed.add_field(name=f"{self.prefix}greet", value="says hello", inline=True)
        embed.add_field(name=f"{self.prefix}search [query]", value="finds and retrieves ten urls based on your search query", inline=True)
        embed.add_field(name=f"{self.prefix}rdt", value="gets a meme from r/memes on Reddit", inline = True)
        embed.add_field(name=f"{self.prefix}ping", value="shows the bot's ping", inline = True)
        embed.add_field(name=f"{self.prefix}workas [job]", value = "assigns you a job", inline=True)
        embed.add_field(name=f"{self.prefix}work", value="complete a small task to get coins, which you can spend in the shop", inline=True)
        embed.add_field(name=f"{self.prefix}bal", value="check your wallet and bank", inline=True)
        embed.add_field(name=f"{self.prefix}dep [amount]", value="deposit some money into your bank", inline=True)
        embed.set_footer(text="shop coming soon || updates on the bot -> https://github.com/moistpotato9873/moistpotatos-bot")
        return embed

    def greet(self):
        """
        Greets the user with a random message.
        """
        return self.GreetList[random.randrange(0, 4, 1)] #randomly select a greeting message

    async def search(self, query, userAgent, msg):
        """
        Searches Google with the user's query. Returns a list with the first ten results.
        """
        fetchedURLS = []
        titles = []
        await msg.edit(content="Searching Google...")
        results = list(googlesearch.search(query, tld="com", num=10, stop=10, pause=2))
        for result in results:
            await msg.edit(content=f"Extracting titles from HTML documents... ({results.index(result)}/{len(results)})")
            fetchedURLS.append(result)
            req = requests.get(result, headers={"User-Agent": userAgent})
            text = BeautifulSoup(req.text, "html.parser")
            title = text.title.text
            titles.append(title)

        return [fetchedURLS, titles]

    def reddit(self):
        """
        Returns a Reddit post in the form of a Discord embed.
        """   
        try:
            self.post += 1
            return self.embeds[self.post]

        except IndexError:
            self.post = 0
            return "out of memes lol"

    def util(self):
        """
        Utility function.

        Returns a string containing the number of embeds, hot posts, the hostname, and the time the posts were last refreshed.
        """
        return f'''
    {len(self.embeds)} embeds
    {len(self.submissions)} hot posts
    last refreshed @ {self.timeLastRefreshed}
    running on {socket.gethostname()}'''

    def startup(self):
        """
        Calls fetch() and records the time spent.
        """
        stop = threading.Event()
        start = time.time()
        self.fetch(stop)
        end = time.time()
        print(f"Fetched all posts in {end-start} seconds.")