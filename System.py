from BasketballReferenceScraper import *
from GoatCalculations import *



# The primary function that is called from main()
def Run():
    # we should make a functionality that allows checks for existing formatted documents to input a top 100 players list
    FinalPlayerList = PullData()
    # Once Data is pulled we should go to Goat calculations to normalize the data to create
    # standardized values for each accolade
    RunFinalCalculations()