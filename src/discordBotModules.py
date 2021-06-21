import time
import random
import threading
import os
import tqdm
import utilityFunctions

try:
    import googlesearch

except ImportError:
    utilityFunctions.botUtilityFunctions().installDependencies(['beautifulsoup4', 'google'])

class discordBotFunctions():
    def __init__(self, reddit, discord):
        self.GreetList = [' Greetings!', ' Hello!', ' Hi!', ' Hey!']
        self.prefix = '.'
        self.version = '0.94'
        self.subreddits = ['memes', 'me_irl', 'dankmemes']
        self.embeds = []
        self.submissions = []
        self.post = None
        self.timeLastRefreshed = None
        self.threads = []
        self.redditObj = reddit
        self.discord = discord
        self.utilFuncs = utilityFunctions.botUtilityFunctions()

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
                    print("sticky")
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
                embed.set_footer(text = f'{self.post.score} ⬆️ | {len(self.post.comments)} 💬')
                self.embeds.append(embed)

        self.post = 0


        if not stop.is_set():
            self.threads.append(threading.Timer(self.utilFuncs.getNextRefreshTime(), self.fetch, [stop]).start()) #set a timer for 8 hours to refresh the posts

    def help(self):
        """
        Returns a list of commands for the bot.
        """
        print(f'{time.asctime()}: We received "{self.prefix}help" command!')
        return f'''Commands for version `{self.version}`:
        **{self.prefix}help** - sends this list of commands
        **{self.prefix}greet** - says hello
        **{self.prefix}search** - finds and retrieves ten urls based on your search query
        **{self.prefix}reddit** - gets a meme from r/memes on Reddit'''

    def greet(self):
        """
        Greets the user with a random message.
        """
        print(f'{time.asctime()}: We received the "{self.prefix}greet" command!')
        return self.GreetList[random.randrange(0, 4, 1)] #randomly select a greeting message

    def search(self, query):
        """
        Searches Google with the user's query. Returns a list with the first ten results.
        """
        fetchedURLS = []
        print(f'{time.asctime()}: We received the "{self.prefix}search" command!')
        for search_results in googlesearch.search(query, tld="com", num=10, stop=10, pause=2):
            fetchedURLS.append(search_results) #add all ten search results to the to-be-returned list

        return [f'''Here are ten URLS based on your search `{query}`:''', fetchedURLS]

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

        Returns a string containing the number of embeds, hot posts, and the time the posts were last refreshed.
        """
        return f'''{len(self.embeds)} embeds
    {len(self.submissions)} hot posts
    last refreshed @ {self.timeLastRefreshed}'''

    def startup(self):
        """
        Calls fetch() and records the time spent.
        """
        stop = threading.Event()
        start = time.time()
        self.fetch(stop)
        end = time.time()
        print(f"Fetched all posts in {end-start} seconds.")
