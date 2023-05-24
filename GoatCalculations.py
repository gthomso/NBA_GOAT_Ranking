from Player import *

PlayerList1 = list()
PlayerList2 = list()
PlayerList3 = list()


def RunningScoreCalc(inputPlayer):
    inputPlayer.runningScore = 4*int(inputPlayer.all_stars) + 5*int(inputPlayer.championships)
    inputPlayer.runningScore += 14*int(inputPlayer.mvp) + 3*int(inputPlayer.asmvp)
    inputPlayer.runningScore += 2*int(inputPlayer.dpoy) + 1*int(inputPlayer.roy)
    inputPlayer.runningScore += 8*int(inputPlayer.finalMVP) + 4*int(inputPlayer.allNBA)
    inputPlayer.runningScore += 3*int(inputPlayer.allDef) + 1*int(inputPlayer.statTitles)
    inputPlayer.runningScore += 9*int(inputPlayer.careerPER)
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