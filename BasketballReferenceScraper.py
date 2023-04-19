from bs4 import BeautifulSoup
import requests
import string
import time
from Player import *

playerList1 = list()
playerList2 = list()
playerList3 = list()
playerNameList = list()

def PullData():
    GetList1()
    

def GetList1():
    tempStrChampionships = ''
    tempStrAllStars = ''
    #finding players with 3+ chips
    html_text = requests.get('https://www.basketball-reference.com/leaders/most_championships.html').text
    FindPlayersWithAtLeast3Chips(html_text)

    # Next we need to add all players with 3 or more All-star games
    #commented the other part out because currently testing the All star portion
    html_text = requests.get('https://www.basketball-reference.com/awards/all_star_by_player.html').text
    FindPlayersAllStarSelections(html_text)

    for each in playerList1:
        tempStrChampionships = str(each.championships)
        tempStrAllStars = str(each.all_stars)
        print(each.name + '\t' + tempStrChampionships + '\t' + tempStrAllStars + '\n')


def FindPlayersWithAtLeast3Chips(html_text):
    tempPlayerName = ''
    soup = BeautifulSoup(html_text, 'lxml')
    groupOfPlayers = soup.find('tbody')
    # Cycles through every player in the list and uses temp variables to store information to
    # PlayerList1
    # currently storing all hall of famers with the * next to them
    for everyPlayer in groupOfPlayers.find_all('td'):
        if everyPlayer.get('data-stat') == 'player':
            tempPlayerName = everyPlayer.get_text()
            tempPlayerName = CleanPlayerName(tempPlayerName)
            playerNameList.append(tempPlayerName)
        elif everyPlayer.get('data-stat') == 'champ_count':
            tempPlayer = Player()
            tempPlayer.name = tempPlayerName
            tempPlayer.championships = everyPlayer.get_text()
            playerList1.append(tempPlayer)
            print(tempPlayer.name + ' ' + tempPlayer.championships + '\n')
    

def FindPlayersAllStarSelections(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    tableOfPlayers = soup.find('table')
    bodyOfPlayers = tableOfPlayers.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexAllStarSelectionNameAndNumber(everyPlayer)
        if tempPlayer.name not in playerNameList:
            playerList1.append(tempPlayer)
        else:
            for each in playerList1:
                if each.name == tempPlayer.name:
                    each.all_stars = tempPlayer.all_stars
                    break
    


def Find_Stats_For_Player():
    print('hi')


# This is just to more easily parse through some names that Basketball reference appends a '*' to
def CleanPlayerName(name):
    if name[-1]=='*':
        name = name[:-1]
    return name

# Helps with indexing to get to the name and number of all star selections a player would have.
def IndexAllStarSelectionNameAndNumber(html_text):
    playerInQuestion = Player()
    tempHtml = html_text.find_all('td')
    playerInQuestion.name = tempHtml[1].get_text()
    playerInQuestion.all_stars = tempHtml[2].get_text()

    return playerInQuestion
