import random

class workFunctions():
    def __init__(self, ):
        self.jobList = ['Doctor', 'Musician', 'Pro Gamer']

    def work(self):
        r = random.randint(0, 2)
        if r == 0:
            workTasks.copypaste()

        elif r == 1:
            workTasks.backwards()
        
        else:
            workTasks.scramble()

    def workas(self, jobName):
        if jobName in self.jobList:
            return True

        else:
            return False

class workTasks():
    def __init__(self):
        self.doctorPhrases = ["Get that apple away from me!", "You will be perscribed with ibuprofen.", "Your heart rate and breathing rate are low."]

    def copypaste(self, jobName):
        if jobName == "Doctor":
            return self.doctorPhrases[random.randint(0, 2)]

    def backwards(self):
        pass

    def scramble(self):
        pass

## ok so maybe in main.py it will search the json file for the username, and the info tied to it. 
# once it gets that, it can use the methods accordingly. 
# the class methods themselves won't have to do any decision making, 
# just because then there's no real way to store the information easily. 
# like you'd basically have to make an object of this class for every single user which is super dumb