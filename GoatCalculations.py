from Player import *
import math

# Player Lists listed here to be utilized globally
PlayerList1 = list()
PlayerList2 = list()
PlayerList3 = list()

# This is the function that is called once we have the data pulled.
def RunFinalCalculations():
    # These are just placeholder players to hold the numbers for each stat.
    mathPlayerSet = ReadTextFile()
    avgPlayer = Player()
    stdDevPlayer = Player()
    avgPlayer = FindAverageForAllCatagories(mathPlayerSet)
    stdDevPlayer = FindStdDevForPlayersCatagories(mathPlayerSet, avgPlayer)
    # Stores the final greatness Stat into the MathPlayerSet List
    CalculateGreatnessStat(mathPlayerSet, avgPlayer, stdDevPlayer)
    # Need to just sort by greatness Stat than print it out
    finalPlayerSet = SortByGreatness(mathPlayerSet)
    PrintList(finalPlayerSet)
    

# Could be refactored if I cared more, but just the function that gets a rough idea for the top 100 players
def RunningScoreCalc(inputPlayer):
    inputPlayer.runningScore = 3.5*int(inputPlayer.all_stars) + 6*int(inputPlayer.championships)
    inputPlayer.runningScore += 13.5*int(inputPlayer.mvp) + 2.5*int(inputPlayer.asmvp)
    inputPlayer.runningScore += 1.5*int(inputPlayer.dpoy) + .5*int(inputPlayer.roy)
    inputPlayer.runningScore += 7.5*int(inputPlayer.finalMVP) + 3.5*int(inputPlayer.allNBA)
    inputPlayer.runningScore += 3.5*int(inputPlayer.allDef) + .5*int(inputPlayer.statTitles)
    inputPlayer.runningScore += round(6*float(inputPlayer.careerPER),2)
    return inputPlayer

# Essentially filters the input list down to the max number of players we would like to remain.
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

# Function called when sorting in FilterPlayerList.
def sortRunningScore(player):
    return player.runningScore


# Going to save all averages as a Player setting to access later
# finds members of the Player class that aren't callable and arent named and cycles through them.
def FindAverageForAllCatagories(mathPlayerList):
    avgPlayer = Player()
    members = [attr for attr in dir(avgPlayer) if not callable(getattr(avgPlayer, attr)) and not attr.startswith("__")]
    for everyMember in members:
        if everyMember != "name":
            setattr(avgPlayer, everyMember, FindAverageForCatagory(mathPlayerList, everyMember))
    return avgPlayer

# Finding the average for the specific catagory.
def FindAverageForCatagory(mathPlayerList, statBeingFound):
    # finds the average of the specified catagory
    runningSum = 0
    player = Player()
    for everyPlayer in mathPlayerList:
        runningSum += float(everyPlayer.__getattribute__(statBeingFound))
    return round(runningSum/len(mathPlayerList), 2)

# Function that finds the stdDev for each catagory for mathPlayerSet.
def FindStdDevForPlayersCatagories(mathPlayerList, avgPlayer):
    stdDevPlayer = Player()
    members = [attr for attr in dir(stdDevPlayer) if not callable(getattr(stdDevPlayer, attr)) and not attr.startswith("__")]
    for everyMember in members:
        if everyMember != "name":
            setattr(stdDevPlayer, everyMember, FindSingularStdDevStat(mathPlayerList, avgPlayer, everyMember))
    return stdDevPlayer

# Finding the stdDev for a single stat type.
def FindSingularStdDevStat(mathPlayerList, avgPlayer, statBeingFound):
    runningSum = 0
    for everyPlayer in mathPlayerList:
        tempDif = float(float(everyPlayer.__getattribute__(statBeingFound)) - float(avgPlayer.__getattribute__(statBeingFound)))
        runningSum += math.pow(tempDif, 2)
    avgDev = runningSum/(len(mathPlayerList) - 1)
    return round(math.sqrt(avgDev), 2)


#Final calculation of the greatness Stat
def CalculateGreatnessStat(mathPlayerList, avgPlayer, stdDevPlayer):
    members = [attr for attr in dir(stdDevPlayer) if not callable(getattr(stdDevPlayer, attr)) and not attr.startswith("__")]
    for everyPlayer in mathPlayerList:
        tempPlayer = Player()
        for eachMember in members:
            stdDevAwayForStat = 0
            if eachMember != "name":
                stdDevAwayForStat = CalculateIndividualGreatnessStat(everyPlayer, eachMember, avgPlayer, stdDevPlayer)
            setattr(tempPlayer, eachMember, stdDevAwayForStat)
        everyPlayer.finalGreatnessScore = round(CalculateAvgOfDeviationsForPlayer(tempPlayer), 2) + 5
        


# This just calculates the amount of standard deviations away from each statistic the player is.
def CalculateIndividualGreatnessStat(PlayerInQuestion, statInQuestion, avgPlayer, stdDevPlayer):
    tempDevs = 0
    tempDiff = float(PlayerInQuestion.__getattribute__(statInQuestion)) - float(avgPlayer.__getattribute__(statInQuestion))
    if tempDiff != 0:
        tempDevs = (tempDiff*float(PlayerInQuestion.__dict__(statInQuestion)))/float(stdDevPlayer.__getattribute__(statInQuestion))
    else:
        return 0
    return tempDevs

# Finds the average deviation that that player is from the norm.
def CalculateAvgOfDeviationsForPlayer(tempPlayer):
    player = Player()
    sumOfDevs = 0
    members = [attr for attr in dir(tempPlayer) if not callable(getattr(tempPlayer, attr)) and not attr.startswith("__")]
    for everyMember in members:
        if everyMember != "name":
            sumOfDevs += tempPlayer.__getattribute__(everyMember)
    # Needs to be -3 to offset the name, runningScore, and GreatnessScore catagories.
    return sumOfDevs/(len(members)-3)

# function put here to read through the text file on hand.
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

# Sorts by the final lists greatness Score.
def SortByGreatness(mathPlayerSet):
    mathPlayerSet.sort(key=SortGreatnessScore, reverse = True)
    return mathPlayerSet

# Called in function immidiately above.
def SortGreatnessScore(player):
    return player.finalGreatnessScore

# Prints the final list sorted by greatness.
def PrintList(PlayerList):
    index = 1
    for everyPlayer in PlayerList:
        print(index, everyPlayer.name, "\tGreatness Score: ", everyPlayer.finalGreatnessScore)
        index += 1
