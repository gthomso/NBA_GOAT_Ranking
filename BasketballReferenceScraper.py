from bs4 import BeautifulSoup
import requests
import string
import time
from GoatCalculations import *

# The player lists help iteratively build the player base, and narrows it down over each iteration.
#playerList1 = list()
#playerList2 = list()
#playerList3 = list()
# the Player Name List is just a tool to insure that we don't have repeats, and is just a quicker way to
# look up the information.
playerNameList = list()


def PullData():
    global PlayerList1, PlayerList2
    indexCounter = 0
    GetList1()
    PlayerList1 = FilterPlayerList(9, 300, PlayerList1)

    InitializePlayerList2()
    GetList2()
    PlayerList2 = FilterPlayerList(18, 150, PlayerList2)
    for each in PlayerList2:
        indexCounter += 1
        tempStrRunningScore = str(each.runningScore)
        print(indexCounter, each.name, str(each.allNBA), tempStrRunningScore)
    

def GetList1():
    #finding players with 3+ chips
    html_text = requests.get('https://www.basketball-reference.com/leaders/most_championships.html').text
    FindPlayersWithAtLeast3Chips(html_text)

    # Next we need to add all players with 3 or more All-star games
    html_text = requests.get('https://www.basketball-reference.com/awards/all_star_by_player.html').text
    FindPlayersAllStarSelections(html_text)

    #Filter past the Bill Walton problem, by adding MVPs
    html_text = requests.get('https://www.basketball-reference.com/awards/mvp.html').text
    FindPlayersMVPs(html_text)


# Refines the existing list and tries to get it under 150 players
# Takes into account all catagories except for cPER and total Championships
def GetList2():
    html_text = requests.get('https://www.basketball-reference.com/awards/all_star_mvp.html').text
    FindPlayerAllStarMVPs(html_text)

    html_text = requests.get('https://www.basketball-reference.com/awards/dpoy.html').text
    FindPlayersDPOY(html_text)

    html_text = requests.get('https://www.basketball-reference.com/awards/roy.html').text
    FindPlayersROY(html_text)

    html_text = requests.get('https://www.basketball-reference.com/awards/finals_mvp.html').text
    FindPlayersFinalsMVP(html_text)

    html_text = requests.get('https://www.basketball-reference.com/awards/all_league.html').text
    FindPlayersAllNBA(html_text)



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
            PlayerList1.append(tempPlayer)
    

def FindPlayersAllStarSelections(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    tableOfPlayers = soup.find('table')
    bodyOfPlayers = tableOfPlayers.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexAllStarSelectionNameAndNumber(everyPlayer)
        if tempPlayer.name not in playerNameList:
            PlayerList1.append(tempPlayer)
            playerNameList.append(tempPlayer.name)
        else:
            for each in PlayerList1:
                if each.name == tempPlayer.name:
                    each.all_stars = tempPlayer.all_stars
                    break
    

def FindPlayersMVPs(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    summaryOfMVPs = soup.find("div", {"id": "all_mvp_summary"})
    tableOfMVPs = summaryOfMVPs.find('table')
    bodyOfPlayers = tableOfMVPs.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexMVPTable(everyPlayer, 1)
        #Bill walton gets through here
        if tempPlayer.name not in playerNameList:
            PlayerList1.append(tempPlayer)
            playerNameList.append(tempPlayer.name)
        else:
            for each in PlayerList1:
                if each.name == tempPlayer.name:
                    each.mvp += int(tempPlayer.mvp)
                    break


def FindPlayerAllStarMVPs(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    summaryOfASMVPs = soup.find("div", {"id": "all_all_star_mvp_summary"})
    tableOfASMVPs = summaryOfASMVPs.find('table')
    bodyOfPlayers = tableOfASMVPs.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexASMVPTable(everyPlayer, 1)
        if tempPlayer.name not in playerNameList:
            PlayerList2.append(tempPlayer)
        else:
            for each in PlayerList2:
                if each.name == tempPlayer.name:
                    each.asmvp += int(tempPlayer.asmvp)
                    break


def FindPlayersDPOY(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    summaryOfDPOYs = soup.find("div", {"id": "all_dpoy_summary"})
    tableOfDPOYs = summaryOfDPOYs.find('table')
    bodyOfPlayers = tableOfDPOYs.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexDPOYTable(everyPlayer, 1)
        if tempPlayer.name not in playerNameList:
            PlayerList2.append(tempPlayer)
        else:
            for each in PlayerList2:
                if each.name == tempPlayer.name:
                    each.dpoy += int(tempPlayer.dpoy)
                    break

def FindPlayersROY(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    nbaROYSection = soup.find("div", {"id": "all_roy_NBA"})
    FindROY(nbaROYSection)
    abaRoySection = soup.find("div", {"id": "all_roy_ABA"})
    FindROY(abaRoySection)


def FindROY(html_text):
    tempPlayer = Player()
    tableOfNBAROYs = html_text.find('table')
    bodyOfPlayers = tableOfNBAROYs.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexROYTables(everyPlayer)
        if tempPlayer.name not in playerNameList:
            PlayerList2.append(tempPlayer)
        else:
            for each in PlayerList2:
                if each.name == tempPlayer.name:
                    each.roy += 1
                    break


def FindPlayersFinalsMVP(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    summaryOfDPOYs = soup.find("div", {"id": "div_finals_mvp_summary"})
    tableOfDPOYs = summaryOfDPOYs.find('table')
    bodyOfPlayers = tableOfDPOYs.find('tbody')
    for everyPlayer in bodyOfPlayers.find_all('tr'):
        tempPlayer = IndexFinalsMVPTable(everyPlayer, 1)
        if tempPlayer.name not in playerNameList:
            PlayerList2.append(tempPlayer)
        else:
            for each in PlayerList2:
                if each.name == tempPlayer.name:
                    each.finalMVP += int(tempPlayer.finalMVP)
                    break

def FindPlayersAllNBA(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    tableOfAllLeague = soup.find('table', {"id" : "awards_all_league"})
    bodyOfPlayers = tableOfAllLeague.find('tbody')
    # Need to get rid of the 'tr' sections with thead class
    for selectionRow in bodyOfPlayers.find_all('tr', {"class" : ""}):
        listOfTableRow = selectionRow.find_all('td')
        teamList = [listOfTableRow[3], listOfTableRow[4], listOfTableRow[5], listOfTableRow[6], listOfTableRow[7]]
        for eachPlayer in teamList:
            tempPlayer = IndexAllLeagueTable(eachPlayer)
            if tempPlayer.name not in playerNameList:
                PlayerList2.append(tempPlayer)
            else:
                for each in PlayerList2:
                    if each.name == tempPlayer.name:
                        each.allNBA += 1
                        break


# This is just to more easily parse through some names that Basketball reference appends a '*' to
def CleanPlayerName(name):
    if name[-1] == '*':
        name = name[:-1]
    if name[-5:] == '(Tie)':
        name = name[:-6]
    return name


# Helps with indexing to get to the name and number of all star selections a player would have.
def IndexAllStarSelectionNameAndNumber(html_text):
    playerInQuestion = Player()
    tempHtml = html_text.find_all('td')
    playerInQuestion.name = tempHtml[1].get_text()
    playerInQuestion.all_stars = tempHtml[2].get_text()

    return playerInQuestion


def IndexMVPTable(html_text, countIndex):
    playerInQuestion = Player()
    playerInQuestion.name = html_text.find('a').get_text()
    tempHtml = html_text.find_all('td')
    playerInQuestion.mvp = tempHtml[countIndex].get_text()

    return playerInQuestion


def IndexASMVPTable(html_text, countIndex):
    playerInQuestion = Player()
    playerInQuestion.name = html_text.find('a').get_text()
    tempHtml = html_text.find_all('td')
    playerInQuestion.asmvp = tempHtml[countIndex].get_text()

    return playerInQuestion


def IndexDPOYTable(html_text, countIndex):
    playerInQuestion = Player()
    playerInQuestion.name = html_text.find('a').get_text()
    tempHtml = html_text.find_all('td')
    playerInQuestion.dpoy = tempHtml[countIndex].get_text()

    return playerInQuestion


def IndexROYTables(html_text):
    PlayerInQuestion = Player()
    temp_html = html_text.find_all('td')
    tempName = temp_html[1].text
    PlayerInQuestion.name = CleanPlayerName(tempName)
    return PlayerInQuestion


def IndexFinalsMVPTable(html_text, countIndex):
    playerInQuestion = Player()
    playerInQuestion.name = html_text.find('a').get_text()
    tempHtml = html_text.find_all('td')
    playerInQuestion.finalMVP = tempHtml[countIndex].get_text()

    return playerInQuestion


def IndexAllLeagueTable(html_text):
    playerInQuestion = Player ()
    playerInQuestion.name = html_text.find('a').get_text()
    
    return playerInQuestion


def InitializePlayerList2():
    global PlayerList2
    PlayerList2 = PlayerList1
    playerNameList.clear()
    for each in PlayerList1:
        playerNameList.append(each.name)
    return
