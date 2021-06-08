import json

class botUtilityFunctions():
    def __init__(self):
        pass

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
        file = '../res/config.json'

        try:
            fetchedPosts = open(file, 'r')
        except FileNotFoundError:
            fetchedPosts = open(file, 'w+') #gotta make a file if there wasn't one already
            raise EmptyJSONFileError(f'''There was no JSON file found at "{file}", or there were no contents in it. Please create or move a file there and include:
            The token for your discord bot (https://discord.com/developers/applications/your-app-id-here/bot)
            The ID of your reddit bot (https://old.reddit.com/prefs/)
            The secret for your reddit bot (same URL as above)
            Your reddit username
            Your reddit password
            
            Until then this bot will not be able to function.
            More information: https://github.com/moistpotato9873/moistpotatos-bot/wiki''')

        char = fetchedPosts.read(1) #check if there even was anything in the file
        fetchedPosts.close()

        with open(file, 'r') as config:
            data = []
            for line in config:
                data.append(json.loads(line))
            config.close()

        return data[0]

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
            GitHub page for more info: https://github.com/moistpotato9873/moistpotatos-bot/wiki'''

class EmptyJSONFileError(Exception):
    pass