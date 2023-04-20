from Player import *

playerList1 = list()
playerList2 = list()
playerList3 = list()


def RunningScoreForFirstIteration(inputPlayer):
    inputPlayer.runningScore = int(inputPlayer.all_stars) + int(inputPlayer.championships)
    return inputPlayer

def FilterPlayerList1():
    tempPlayerList = list()
    for everyPlayer in playerList1:
        everyPlayer = RunningScoreForFirstIteration(everyPlayer)
        if everyPlayer.runningScore >= 3:
            tempPlayerList.append(everyPlayer)
    return tempPlayerList

