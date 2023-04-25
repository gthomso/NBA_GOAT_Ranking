from Player import *

PlayerList1 = list()
PlayerList2 = list()
PlayerList3 = list()


def RunningScoreCalc(inputPlayer):
    inputPlayer.runningScore = 4*int(inputPlayer.all_stars) + 5*int(inputPlayer.championships)
    inputPlayer.runningScore += 15*int(inputPlayer.mvp) + 4*int(inputPlayer.asmvp)
    inputPlayer.runningScore += 3*int(inputPlayer.dpoy) + 2*int(inputPlayer.roy)
    return inputPlayer


def FilterPlayerList(runningScoreMin, maxPlayers, playerList):
    tempPlayerList = list()
    for everyPlayer in playerList:
        everyPlayer = RunningScoreCalc(everyPlayer)
        # Arbitrary cut off to be determined later
        if everyPlayer.runningScore >= runningScoreMin:
            tempPlayerList.append(everyPlayer)
            if len(tempPlayerList) >= maxPlayers:
                tempPlayerList.sort(key=sortRunningScore, reverse = True)
                return tempPlayerList
    return tempPlayerList


def sortRunningScore(player):
    return player.runningScore