import time
import random
import googlesearch
import threading
import os
import tqdm

class discordBotFunctions():
    def __init__(self, reddit, discord):
        self.GreetList = ['Greetings!', 'Hello!', 'Hi!', 'Hey!']
        self.prefix = '.'
        self.version = '0.94'
        self.embeds = []
        self.hot_posts = []
        self.current_meme = None
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
        subreddit = self.redditObj.subreddit('memes')
        self.hot_posts = list(subreddit.hot(limit=101)) #retrieves posts from reddit and puts them in a list

        for posts in tqdm.tqdm(range(len(self.hot_posts)-1), desc = "Fetching posts..."): #not sure why i have to subtract one post but the program crashes if i don't
            self.current_meme = self.hot_posts[posts]
            if not self.current_meme.stickied:
                #creates embed to be used on discord
                embed = self.discord.Embed(
                    title = self.current_meme.title,
                    url = self.current_meme.name
                )
                embed.set_image(url = self.current_meme.url)
                embed.set_footer(text = f'{self.current_meme.score} ⬆️ | {len(self.current_meme.comments)} 💬')
                self.embeds.append(embed)

            else:
                print("sticky") #post was pinned by r/memes mods, and not an actual post
                self.hot_posts.remove(self.current_meme)

        self.current_meme = 0

        if not stop.is_set():
            # 28800 seconnds is 8 hours
            self.threads.append(threading.Timer(28800, self.fetch, [stop]).start()) #set a timer for 8 hours to refresh the posts

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
        print(f'{time.asctime()}: We received the "{self.prefix}search" command!')
        for search_results in googlesearch.search(query, tld="com", num=10, stop=10, pause=2):
            fetchedURLS.append(search_results) #add all ten search results to the to-be-returned list

        return [f'''Here are ten URLS based on your search `{query}`:''', fetchedURLS]

    def reddit(self):
        """
        Returns a Reddit post in the form of a Discord embed.
        """   
        try:
            return self.embeds[self.current_meme]
            self.current_meme += 1

        except IndexError:
            self.current_meme = 0
            return "out of memes lol"

    def util(self):
        """
        Utility function.

        Returns a string containing the number of embeds, hot posts, and the time the posts were last refreshed.
        """
        return f'''{len(self.embeds)} embeds
        {len(self.hot_posts)} hot posts
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
