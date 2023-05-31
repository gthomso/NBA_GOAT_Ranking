from Player import *
import statistics

# Trying to move the Player Lists into System
PlayerList1 = list()
PlayerList2 = list()
PlayerList3 = list()


def RunningScoreCalc(inputPlayer):
    inputPlayer.runningScore = 4*int(inputPlayer.all_stars) + 5*int(inputPlayer.championships)
    inputPlayer.runningScore += 14*int(inputPlayer.mvp) + 3*int(inputPlayer.asmvp)
    inputPlayer.runningScore += 2*int(inputPlayer.dpoy) + 1*int(inputPlayer.roy)
    inputPlayer.runningScore += 8*int(inputPlayer.finalMVP) + 4*int(inputPlayer.allNBA)
    inputPlayer.runningScore += 4*int(inputPlayer.allDef) + 1*int(inputPlayer.statTitles)
    inputPlayer.runningScore += round(7*float(inputPlayer.careerPER),2)
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
def FindAverageForAllCatagories(inputPlayerList):
    avgPlayer = Player()

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
#ReadTextFile()