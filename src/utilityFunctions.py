import json
import os
import time
from datetime import datetime

class botUtilityFunctions():
    def __init__(self):
        #file path for retrieveJSONContent()
        path = os.path.normpath(__file__ + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'res')
        os.makedirs(path, exist_ok=True)
        self.file = path + os.sep + 'config.json'

        # units of time in milliseconds
        self.millisecond = 1/1000
        self.second = 1
        self.minute = self.second*60
        self.hour = self.minute*60
        self.day = self.hour*24
        self.week = self.day*7
        self.year = self.week*52

        self.refreshHour = 24

    def retrieveJSONContent(self):
        """
        Reads a JSON file for:

        Discord bot token
        Reddit bot ID
        Reddit bot secret
        Reddit username
        Reddit password

        Note that this file is in .gitignore, but the file is created automatically. You will have to include the information yourself, however.
        """
        try:
            fetchedPosts = open(self.file, 'r')
        except FileNotFoundError:
            fetchedPosts = open(self.file, 'w+') #gotta make a file if there wasn't one already
            raise EmptyJSONFileError(self.file)

        char = fetchedPosts.read(1) #check if there even was anything in the file
        fetchedPosts.close()

        with open(self.file, 'r') as config:
            data = []
            for line in config:
                data.append(json.loads(line))
            config.close()

        try:
            return data[0]
        
        except IndexError:
            raise EmptyJSONFileError()

    def installDependencies(self, modules):
        """
        Installs required dependencies.
        """
        print('Installing needed modules...')
        for module in modules:
            print(f'Installing {module}...')
            os.system(f'python3 -m pip install {module} -q')

    def errorOccured(self, author, errorMessage):
        """
        Called when an error occurs relating to Discord.

        Returns a string that is DMed to the user that caused the error.
        """
        print(f"ERROR @ {time.asctime()}: {author} caused {str(errorMessage)}")
        return f'''Something went wrong! Here's the full error message:
        `{str(errorMessage)}`\n
Please submit a bug report here if you're unsure of how to fix the problem: https://forms.gle/owaquH8JPGzhM1DJ6
GitHub page for more info: https://github.com/moistpotato9873/moistpotatos-bot/wiki#faq'''

    # def getHours(self):
    #     """
    #     Attempting to manually get number of hours instead of using datetime.
    #     """
        
    #     now = time.time()
    #     # Years = now / self.year
    #     # print("years: " + str(Years))
    #     # Weeks = now / self.week
    #     # print("weeks: " + str(Weeks))
    #     # Days = now / self.day
    #     # print("days: " + str(Days))
    #     # print(self.hour)
    #     # Hours = now / self.hour
    #     # print("hours: " + str(Hours))
    #     # Minutes = now / self.minute
    #     # print("minutes " + str(Minutes))
    #     # Seconds = now / self.second
    #     # print("seconds: " + str(Seconds))

    #     # getHours = now-Hours

    #     # print(now)
    #     # print(getHours)

    #     # hours = self.refreshHour*self.hour
    #     # print(hours)
    #     # midnight = now-self.day-self.hour-self.minute-self.second-self.millisecond
    #     # print("midnight: " + str(midnight / self.year / self.week / self.day / self.hour / self.minute / self.second / self.millisecond))
    #     # nextRefreshHour = midnight + hours
    #     # print("next refresh hour: " + str(nextRefreshHour))
        
    #     # timeToNextRefresh = nextRefreshHour-now
    #     # print(f"now: {now}")
    #     # print(f"next time to refresh: {str(timeToNextRefresh)} sec ({str(timeToNextRefresh / self.hour)} hrs)")

    def getNextRefreshTime(self):
        """
        Calculate how long to wait until refreshing.
        Refresh timing can sometimes be imprecise, this will prevent it from offsetting.
        """
        now = time.time()
        d = datetime.now()
        hrs = d.hour*self.hour
        mins = d.minute*self.minute
        secs = d.second*self.second

        midnight = now-hrs-mins-secs
        refreshHr = self.refreshHour*self.hour
        execTime = midnight+refreshHr
        timeToNextRefresh = execTime-now
        print("Scheduled to refresh at " + str(timeToNextRefresh))
        self.refreshHour += 8

        if self.refreshHour >= 24:
            self.refreshHour == 0

        return timeToNextRefresh



class EmptyJSONFileError(Exception):
    def __init__(self, filePath):
        self.file = filePath
        print(f'''There was no JSON file found at "{self.file}", or there were no contents in it. Please create or move a file there and include:
            The token for your discord bot (https://discord.com/developers/applications/your-app-id-here/bot)
            The ID of your reddit bot (https://old.reddit.com/prefs/apps)
            The secret for your reddit bot (same URL as above)
            Your reddit username
            Your reddit password

            Until then this bot will not be able to function.
            More information: https://github.com/moistpotato9873/moistpotatos-bot/wiki''')
