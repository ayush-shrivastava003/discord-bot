# moistpotato's bot

(from the [wiki](https://github.com/moistpotato9873/wiki))

moistpotato's bot is a template for new programmers like myself to program a Discord bot! It's written entirely in Python for simplicity. It features basic functions, a connection to the Reddit and Google APIs, and is designed to be as user-friendly as possible. This will cover everything you need to know about the bot.

Invite the bot [here](https://discord.com/oauth2/authorize?client_id=806934438738264114&scope=bot) 

## table of contents
* [developers - setting up the bot](https://github.com/moistpotato9873/moistpotatos-bot/wiki/#developers---setting-up-the-bot)
* [faq](https://github.com/moistpotato9873/moistpotatos-bot/wiki/#faq)
* [rules for use](https://github.com/moistpotato9873/moistpotatos-bot/wiki/#rules-for-use)
* [credits](https://github.com/moistpotato9873/moistpotatos-bot/wiki/#credits)

## developers - setting up the bot

This bot is designed with simplicity in mind. I'm definitely not the best programmer, but I have tried my best to make this as simple and easy as possible to set up. I'll go over how to do this.

**Note that this bot will require your reddit username and password to function. If you choose to upload your own version of this bot to GitHub, add `config.json` to `.gitignore.`**

#### read over the rules

Please read over the rules for using this first. You can use this bot template however you want, but I'd like some credit. Those rules will prevent my work from being taken without credit.

#### download the latest release

Once you've followed all the instructions in the rules section, download the latest release in the Releases section. This will let you get all the code without cloning the repo.

#### register new discord/reddit bots

You'll need to register a discord bot and a reddit bot in order to access their APIs. Let's start with Discord:

1. Go to https://discord.com/developers

2. Click "New Application"

![new-app](https://cdn.discordapp.com/attachments/808703949720387584/854455994233651261/unknown.png)

3. Enter the name of your bot and click "Create"

![create-button](https://cdn.discordapp.com/attachments/808703949720387584/854456315429912617/unknown.png)

4. In your new application, navigate to the "Bot" tab and add a new bot.

![new-bot](https://cdn.discordapp.com/attachments/808703949720387584/854456527997239296/unknown.png)

5. Add an icon and username for your bot.

![icon](https://cdn.discordapp.com/attachments/808703949720387584/854455631028027392/unknown.png)

6. Under your bot's username, copy the token. You'll need this later.

![token](https://cdn.discordapp.com/attachments/808703949720387584/854459238399213618/unknown.png)

6. Make sure these settings match yours:

![settings](https://cdn.discordapp.com/attachments/808703949720387584/854455312895705088/Screenshot_2021-06-15_162012.jpg)

Now for Reddit:

1. Go to https://old.reddit.com/prefs/apps

2. Create a new app. Enter the name and select "script".

![new-app](https://cdn.discordapp.com/attachments/808703949720387584/854457331978076240/unknown.png)

3. Click "create app"

4. Under "developed applications", find your app and click "edit"

![edit](https://cdn.discordapp.com/attachments/808703949720387584/854458439304609873/Screenshot_2021-06-15_163201.jpg)

5. Your client ID and secret will show (ID indicated in red, secret in blue). Copy those for later.

![id-and-secret](https://cdn.discordapp.com/attachments/808703949720387584/854458962661736478/Screenshot_2021-06-15_163438.jpg)

6. Construct a user agent. According to the [Reddit API rules](https://github.com/reddit-archive/reddit/wiki/API#rules), you need a user agent to be able to access their API. The page I linked tells you how to make one.

This should be everything you need for registering Discord and Reddit bots.

#### include your bot information

Navigate to the /res/ folder and create a new file called "config.json". You'll need a few things for this (not in any specific order, but they all need to be there):

* The token for your Discord bot (step 6)
* The client ID for your Reddit bot (step 4 and 5)
* The client secret for your Reddit bot (step 4 and 5)
* The user agent for your Reddit bot (step 6)
* Your Reddit username
* Your Reddit password

Add this information in this format with these keywords:

    {"token": "your discord token", "client_id": "your client id", "client_secret": "your client secret", "user_agent": "your user agent", "username": "your reddit username", "password": "your reddit password"}`

Once again, remember to add this file to .gitignore if you're uploading it to GitHub. This information can cause someone else to configure your bot and enter your Reddit account.

#### start up the bot

Go to your terminal and type the absolute path to the source folder.

*For Mac or Linux:*

    cd "~/projects/moistpotatos-bot/src/"

*For Windows:*

    cd "C:/projects/moistpotatos-bot/src/"

Next, run `main.py` using the terminal command.

*For Mac or Linux:* `python3 main.py`

*For Windows:* `py main.py`

If you're encountering an error that says that "py" or "python3" is not recognized, make sure you have installed Python properly. In the installer it will ask you if you want to add it to the environment variables.

#### invite your bot

The basic layout of a bot invite link is this:

    https://discord.com/oauth2/authorize?client=yourbotidhere&scope=bot

You can get your bot's ID under the general information tab for your application.

## faq

* Am I allowed to use this code?

Yes! You may use this code as long as you agree to the rules for use (including signing the form). Please keep the credits to this repo in the code :)

* How do I use this bot?

Here are all the current commands:

1.    **.help** - sends this list of commands
2.    **.greet** - says hello
3.    **.search** - finds and retrieves ten URLs based on your search query
4.    **.reddit** - sends a Reddit post from https://reddit.com/r/memes

* The bot is acting weirdly/DMed me. What should I do?

If the bot is being buggy, or DMed you about an error, please submit a [bug report](https://forms.gle/owaquH8JPGzhM1DJ6). I'll send you an email telling you how to fix the problem.

* How do I invite the bot/share it with others?

The invite link can be found [here](https://discord.com/oauth2/authorize?client_id=806934438738264114&scope=bot). I'd really appreciate it if you shared this repo with others :)

## rules for use

This code can be used an modified, but I do have some rules if you're going to do so:

1. You credit me and include this repo link in the help command, the error DM, your repo, etc.
2. You will not use this code in any commercial setting.
3. If you are modifying this code, it needs to be uploaded to a repo.
4. I am not responsible for any damages or leaked personal info.
5. You submit [this form](https://forms.gle/adpT1YSL6jGvTzuf9) telling me that you want to use my code.

## credits

[discord.py](https://https://discordpy.readthedocs.io/) - for providing the most essential code for the bot: the connection to the Discord API

[PRAW](https://praw.readthedocs.io/) - for providing simple access to the Reddit API

[googlesearch](https://www.geeksforgeeks.org/performing-google-search-using-python-code/) - for providing simple access to the Google API

Thanks for reading through this whole thing!