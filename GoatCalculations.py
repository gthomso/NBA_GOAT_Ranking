from Player import *

firstPlayerList = list()
FinalList = list()


def RunningScoreForFirstIteration(inputPlayer):
    inputPlayer.runningScore = 3*int(inputPlayer.all_stars) + 6*int(inputPlayer.championships)
    inputPlayer.runningScore += 15*int(inputPlayer.mvp)
    return inputPlayer

def FilterPlayerList1():
    tempPlayerList = list()
    for everyPlayer in firstPlayerList:
        everyPlayer = RunningScoreForFirstIteration(everyPlayer)
        # Arbitrary cut off to be determined later
        if everyPlayer.runningScore >= 11:
            tempPlayerList.append(everyPlayer)
    return tempPlayerList

