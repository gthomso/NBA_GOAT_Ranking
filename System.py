from BasketballReferenceScraper import *
from GoatCalculations import *
import os
import cmd



# The primary function that is called from main()
# First checks pathing for if there is a text file to read from. If not it will create a new one
# No matter what path it takes it will evantually have the complete data set and will Calculate the gratness Score
def Run():
    # Seeing if txt file exists
    currentPath = os.getcwd()
    if os.path.exists(currentPath + '\\PlayerInfo.txt'):
        # Gives a option to user to use new file
        print("Player file found. Do you wish to scan existing file or create new one?")
        print("enter 1 for using existing file")
        print("Enter 2 for new file, may take around 6 minutes")
        inputInfo = input()
        print("thank you\n")
        if inputInfo == '1':
            RunFinalCalculations()
        elif inputInfo == '2':
            PullData()
            RunFinalCalculations()
        else:
            print("sorry input is not recognized")
    else:
        print("This will take around 6 minutes")
        PullData()
        RunFinalCalculations()