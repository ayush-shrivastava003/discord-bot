import json
import os
import time
import sys
from datetime import datetime

class botUtilityFunctions():
    def __init__(self):
        #file path for retrieveJSONContent()
        path = os.path.normpath(__file__ + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'res')
        os.makedirs(path, exist_ok=True)
        self.file = path + os.sep + 'config.json'

        self.configTemplate = {
                                "bot_info": {
                                    "token": "none",
                                    "username": "none",
                                    "password": "none",
                                    "client_id": "none",
                                    "client_secret": "none",
                                    "user_agent": "none"
                                },
                                "user_info": {}
                            }

        # units of time in milliseconds
        self.millisecond = 1/1000
        self.second = 1
        self.minute = self.second*60
        self.hour = self.minute*60
        self.day = self.hour*24
        self.week = self.day*7
        self.year = self.week*52

        self.refreshHour = 16

    def retrieveJSONContent(self, key=None):
        """
        Reads a JSON file for:

        Discord bot token
        Reddit bot ID
        Reddit bot secret
        Reddit username
        Reddit password
        Reddit user agent

        Note that this file is in .gitignore, but the file is created automatically. You will have to include the information yourself, however.
        """
        if not os.path.exists(self.file):
            config = open(self.file, "w+")
            json.dump(self.configTemplate, self.file)
            config.close()

            raise FileNotFoundError(f'''There was no JSON file found at "{self.file}". One has automatically been made for you, but you need to include some of your own information:
            The token for your discord bot (https://discord.com/developers/applications/your-app-id-here/bot)
            The ID of your reddit bot (https://old.reddit.com/prefs/apps)
            The secret for your reddit bot (same URL as above)
            Your reddit username
            Your reddit password

            Until then this bot will not be able to function.
            More information: https://github.com/moistpotato9873/moistpotatos-bot/wiki#developers---setting-up-the-bot''')

        with open(self.file, 'r') as config:
            data = json.loads(config.read())

        try:
            if key:
                return data[key]

            else:
                return data
        
        except KeyError as e:
            print("key error: " + str(e))
            self.dumpToJSON(key)
            return False

    def installDependencies(self, modules):
        """
        Installs required dependencies.
        """
        print('Installing needed modules...')

        if sys.platform == 'win32':
            name = 'py'
        
        else:
            name = 'python3'

        for module in modules:
            print(f'Installing {module}...')
            os.system(f'{name} -m pip install {module} -q')

        print("Finished installing modules.\n")

    def errorOccured(self, author, errorMessage):
        """
        Called when an error occurs relating to Discord.

        Returns a string that is DMed to the user that caused the error.
        """
        print(f"ERROR @ {time.asctime()}: {author} caused {str(errorMessage)}")
        return f'''Something went wrong! Here's the full error message:
        `{str(errorMessage)}`\n
Please submit a bug report here if you're unsure of how to fix the problem: https://forms.gle/owaquH8JPGzhM1DJ6
Or, if you have a GitHub profile, create an issue at the repository linked below.
GitHub page for more info: https://github.com/moistpotato9873/moistpotatos-bot/wiki#faq'''

    def dumpToJSON(self, authorID: str, newWorkData:dict=None, newMoneyData:dict=None):
        with open(self.file, 'r+') as config:
            JSONContent = self.retrieveJSONContent()
            
            if authorID not in JSONContent["user_info"]: # user is not in our records so we need to create a new 
                userTemplate = {"work_info": {"hours": 0, "job": "none", "cpstring": "none", "lastWorkCmd": True}, "money_info": {"wallet": 0, "bank": 0, "bankSpace": 1000}}
                JSONContent["user_info"][authorID] = userTemplate

            if newWorkData is not None:
                JSONContent["user_info"][authorID]["work_info"].update(newWorkData)
                
            if newMoneyData is not None: # other data that is not work details
                JSONContent["user_info"][authorID]["money_info"].update(newMoneyData)
            
            config.seek(0)
            json.dump(JSONContent, config)
            config.truncate()


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
        nextRefreshHr = timeToNextRefresh / self.hour
        print(f"Scheduled to refresh in {timeToNextRefresh} seconds ({nextRefreshHr} hours)")

        if self.refreshHour >= 24:
            self.refreshHour = 0

        self.refreshHour += 8

        return timeToNextRefresh

    def splitList(self, list):
        listHalf = len(list)//2
        return list[:listHalf], list[listHalf:]