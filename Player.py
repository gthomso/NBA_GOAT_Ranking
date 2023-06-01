# Main class used to hold most of the data that we need during this project
class Player:
    def __init__(self) -> None:
        pass
        
    # Used later for the values used in calculations.
    def __dict__(self, key):
        playerStatWeightDict = {"all_stars" : 3.5, "championships" : 6, 
                                "mvp" : 13.5, "asmvp" : 2.5, "dpoy" : 1.5,
                                "roy" : .5, "finalMVP" : 7.5, "allNBA" : 3.5,
                                "allDef" : 3.5, "statTitles" : .5, "careerPER" : 6,
                                "finalGreatnessScore" : 0, "runningScore" : 0}
        return playerStatWeightDict[key]
    
    # Each of the stats that we track, plus name, a running score for when pulling the data on 100
    # players, and the final Greatness Score.
    name = ''
    all_stars = 0
    championships = 0
    mvp = 0
    dpoy = 0
    roy = 0
    asmvp = 0
    finalMVP = 0
    allNBA = 0
    allDef = 0
    statTitles = 0
    careerPER = 0
    runningScore = 0
    finalGreatnessScore = 0
    