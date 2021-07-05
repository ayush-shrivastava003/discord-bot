from utilityFunctions import botUtilityFunctions
import random

class work():
    def __init__(self):
        self.utilFuncs = botUtilityFunctions()
        self.jobList = ["Doctor", "Pro Gamer", "Among Us Crewmate"]
        self.cpstrings = {
                        "Doctor": 
                            [
                                "Get that apple away from me!",
                                "You will need to be prescribed with ibuprofen",
                                "Your breathing rate is low."
                            ],
                        "Pro Gamer":
                            [
                                "snort gfuel",
                                "follow me on my twitch twitch.tv/fortnitechungus1234",
                                "EPIC CLIP HIGHLIGHTS ON YOUTUBE"
                            ],
                        "Among Us Crewmate":
                            [
                                "red is so sus rn",
                                "OMG UR SO SUS!!!!!!!!!!!!!!! EMERGENCY MEETING! EMERGENCY MEETING!",
                                "GET OUT OF MY HEAD GET OUT OF MY HEAD GET OUT OF MY HEAD GET OUT OF MY HEAD"
                            ]
                        }

    def query(self, user, query=None):
        userInfo = self.utilFuncs.retrieveJSONContent(key="user_info")
        if user in userInfo:
            userInfo = userInfo[user]

            if query and userInfo:
                return userInfo[query]

            elif userInfo:
                return userInfo
            
            else:
                return False
        
        else:
            return False

    def work(self, user):
        userInfo = self.query(user, query="work_info")
        if userInfo:
            currentJob = userInfo["job"]
            if currentJob == "none":
                return False
            
            else:
                userInfo["hours"] += 1
                selectedString = self.cpstrings[currentJob][random.randrange(0, 2)]
                userInfo["cpstring"] = selectedString
                userInfo["lastWorkCmd"] = True
                self.utilFuncs.dumpToJSON(user, newWorkData=userInfo)
                fullString = f"**Work as a(n) {currentJob}**\nCopy the following phrase: `{selectedString}`"
                return fullString
        

    def workas(self, job):
        if job in self.jobList:
            return True

        else:
            return False

    def checkCP(self, authorID, msg):
        user = self.query(authorID)
        user["work_info"]["lastWorkCmd"] = False
        if msg == user["work_info"]["cpstring"].lower():
            user["money_info"]["wallet"] += 500
            user["work_info"]["cpstring"] = "none"
            self.utilFuncs.dumpToJSON(authorID, newMoneyData=user["money_info"], newWorkData=user["work_info"])
            return "nice, you get `500` coins from that"

        else:
            self.utilFuncs.dumpToJSON(authorID, newMoneyData=user["money_info"], newWorkData=user["work_info"])
            return "HHHAHAHAHA U MESSED UP WHILE TRYING TO WORK LLLLLLLLLLL so bad :clown::clown::clown::clown:"