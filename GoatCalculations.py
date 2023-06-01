from Player import *
import statistics
import math

# Trying to move the Player Lists into System
PlayerList1 = list()
PlayerList2 = list()
PlayerList3 = list()


def RunFinalCalculations():
    # These are just placeholder players to hold the numbers for each stat.
    mathPlayerSet = ReadTextFile()
    avgPlayer = Player()
    stdDevPlayer = Player()
    avgPlayer = FindAverageForAllCatagories(mathPlayerSet)
    stdDevPlayer = FindStdDevForPlayersCatagories(mathPlayerSet, avgPlayer)



def RunningScoreCalc(inputPlayer):
    inputPlayer.runningScore = 3.5*int(inputPlayer.all_stars) + 6*int(inputPlayer.championships)
    inputPlayer.runningScore += 13.5*int(inputPlayer.mvp) + 2.5*int(inputPlayer.asmvp)
    inputPlayer.runningScore += 1.5*int(inputPlayer.dpoy) + .5*int(inputPlayer.roy)
    inputPlayer.runningScore += 7.5*int(inputPlayer.finalMVP) + 3.5*int(inputPlayer.allNBA)
    inputPlayer.runningScore += 3.5*int(inputPlayer.allDef) + .5*int(inputPlayer.statTitles)
    inputPlayer.runningScore += round(6*float(inputPlayer.careerPER),2)
    return inputPlayer


def FilterPlayerList(runningScoreMin, maxPlayers, playerList):
    tempPlayerList = list()
    indexCounter = 0
    for everyPlayer in playerList:
        everyPlayer = RunningScoreCalc(everyPlayer)
        # Arbitrary cut off to be determined later
        if everyPlayer.runningScore >= runningScoreMin:
            tempPlayerList.append(everyPlayer)
    tempPlayerList.sort(key=sortRunningScore, reverse = True)
    if len(tempPlayerList) >= maxPlayers:
        tempPlayerList = tempPlayerList[:maxPlayers]
    return tempPlayerList


def sortRunningScore(player):
    return player.runningScore


# Going to save all averages as a Player setting to access later
def FindAverageForAllCatagories(mathPlayerList):
    avgPlayer = Player()
    members = [attr for attr in dir(avgPlayer) if not callable(getattr(avgPlayer, attr)) and not attr.startswith("__")]
    for everyMember in members:
        if everyMember != "name":
            setattr(avgPlayer, everyMember, FindAverageForCatagory(mathPlayerList, everyMember))
    #avgPlayer.all_stars = FindAverageForCatagory(mathPlayerList, "all_stars")
    return avgPlayer


def FindAverageForCatagory(mathPlayerList, statBeingFound):
    # finds the average of the specified catagory
    runningSum = 0
    player = Player()
    for everyPlayer in mathPlayerList:
        runningSum += float(everyPlayer.__getattribute__(statBeingFound))
    return round(runningSum/len(mathPlayerList), 2)


def FindStdDevForPlayersCatagories(mathPlayerList, avgPlayer):
    stdDevPlayer = Player()
    members = [attr for attr in dir(stdDevPlayer) if not callable(getattr(stdDevPlayer, attr)) and not attr.startswith("__")]
    for everyMember in members:
        if everyMember != "name":
            setattr(stdDevPlayer, everyMember, FindSingularStdDevStat(mathPlayerList, avgPlayer, everyMember))
    return stdDevPlayer


def FindSingularStdDevStat(mathPlayerList, avgPlayer, statBeingFound):
    runningSum = 0
    for everyPlayer in mathPlayerList:
        tempDif = float(float(everyPlayer.__getattribute__(statBeingFound)) - float(avgPlayer.__getattribute__(statBeingFound)))
        runningSum += math.pow(tempDif, 2)
    avgDev = runningSum/(len(mathPlayerList) - 1)
    return round(math.sqrt(avgDev), 2)


#Final calculation of the greatness Stat
def CalculateGreatnessStat():

    return


def ReadTextFile():
    mathPlayerList = list()
    top100File = open("PlayerInfo.txt", "r")
    for line in top100File:
        tempPlayer = Player()
        playerRawData = line.split(",")
        tempPlayer.name = playerRawData[0]
        tempPlayer.all_stars = playerRawData[1]
        tempPlayer.championships = playerRawData[2]
        tempPlayer.mvp = playerRawData[3]
        tempPlayer.dpoy = playerRawData[4]
        tempPlayer.roy = playerRawData[5]
        tempPlayer.asmvp = playerRawData[6]
        tempPlayer.finalMVP = playerRawData[7]
        tempPlayer.allNBA = playerRawData[8]
        tempPlayer.allDef = playerRawData[9]
        tempPlayer.statTitles = playerRawData[10]
        tempPlayer.careerPER = playerRawData[11]
        mathPlayerList.append(tempPlayer)
    top100File.close()
    return mathPlayerList

#used for testing when the file has been built.
RunFinalCalculations()