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
    global PlayerList1, PlayerList2, PlayerList3
    indexCounter = 0
    GetList1()
    PlayerList1 = FilterPlayerList(9, 300, PlayerList1)

    InitializePlayerList2()
    GetList2()
    PlayerList2 = FilterPlayerList(18, 150, PlayerList2)

    InitializePlayerList3()
    GetList3()
    PlayerList3 = FilterPlayerList(36, 100, PlayerList3)
    
    for each in PlayerList3:
        indexCounter += 1
        tempStrRunningScore = str(each.runningScore)
        print(indexCounter, each.name, str(each.careerPER), tempStrRunningScore)
    

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

    html_text = requests.get('https://www.basketball-reference.com/awards/all_defense.html').text
    FindPlayersAllDefense(html_text)


def GetList3():
    # Need to go through every name to find stat leaders, cPER and Total championships
    # should add stats up here to the players in player list 3.
    print("[", end='')
    for eachPlayer in PlayerList3:
        tempPlayer = Player()
        tempName = eachPlayer.name
        tempPlayerFullName = ParseName(tempName)
        builtURL = BuildPlayerURL(tempPlayerFullName)
        # This calls the Calling of the specific player data.
        tempPlayer = EnsureUrlIsCorrect(builtURL, tempName)

        eachPlayer.statTitles = tempPlayer.statTitles
        eachPlayer.careerPER = tempPlayer.careerPER        
        print(".",end='')

        time.sleep(2.4)
    print("]")
        
        

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
            tempPlayer = IndexAllLeagueAwardsTables(eachPlayer)
            if tempPlayer.name not in playerNameList:
                PlayerList2.append(tempPlayer)
            else:
                for each in PlayerList2:
                    if each.name == tempPlayer.name:
                        each.allNBA += 1
                        break


def FindPlayersAllDefense(html_text):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    tableOfAllLeague = soup.find('table', {"id" : "awards_all_defense"})
    bodyOfPlayers = tableOfAllLeague.find('tbody')
    # Need to get rid of the 'tr' sections with thead class
    for selectionRow in bodyOfPlayers.find_all('tr', {"class" : ""}):
        listOfTableRow = selectionRow.find_all('td')
        teamList = [listOfTableRow[3], listOfTableRow[4], listOfTableRow[5], listOfTableRow[6], listOfTableRow[7]]
        for eachPlayer in teamList:
            tempPlayer = IndexAllLeagueAwardsTables(eachPlayer)
            if tempPlayer.name not in playerNameList:
                PlayerList2.append(tempPlayer)
            else:
                for each in PlayerList2:
                    if each.name == tempPlayer.name:
                        each.allDef += 1
                        break


# This serves as a way to find all the data on the players specific page.
def FindPlayerSpecificData(html_text, tempName):
    tempPlayer = Player()
    soup = BeautifulSoup(html_text, 'lxml')
    allPlayerAccomplishments = soup.find('ul', {"id" : "bling"})
    tempPlayer.statTitles = FindPlayerStatTitles(allPlayerAccomplishments)
    careerPERHtml = soup.find('div', {"class" : "p3"})
    tempPlayer.careerPER = FindPlayerCareerPer(careerPERHtml)
    return tempPlayer



def FindPlayerStatTitles(html_text):
    allStatTitles = 0
    for eachStatTitle in html_text.find_all('li', {"class" : "poptip"}):
        howManyTitles = eachStatTitle.find('a').get_text()
        allStatTitles += FindHowManyStatTitles(howManyTitles)
    return allStatTitles

# Need to figure out how many titles are there in the raw text
def FindHowManyStatTitles(howManyStatTitles):
    tempAmount = 0
    tempString = howManyStatTitles.split(" ")
    if tempString[0][-1] == 'x':
        tempAmount = int(tempString[0][:-1])
    else:
        tempAmount = 1
    return tempAmount


def FindPlayerCareerPer(html_text):
    eachEntry = html_text.find_all('p')
    perStatForPlayer = eachEntry[1].get_text()
    return perStatForPlayer

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


def IndexAllLeagueAwardsTables(html_text):
    playerInQuestion = Player ()
    if html_text.get_text():
        playerInQuestion.name = html_text.find('a').get_text()
    
    return playerInQuestion




def InitializePlayerList2():
    global PlayerList2
    PlayerList2 = PlayerList1
    playerNameList.clear()
    for each in PlayerList1:
        playerNameList.append(each.name)
    return


def InitializePlayerList3():
    global PlayerList3
    PlayerList3 = PlayerList2
    playerNameList.clear()
    for each in PlayerList2:
        playerNameList.append(each.name)
    return

def ParseName(name):
    # For players names who have an ' in it eg. Shaquille O'Niel
    name = ''.join(name.split("'"))
    # For players from foriegn lands with unrecognized ascii
    name = 'c'.join(name.split("ć"))
    name = 'o'.join(name.split("ó"))
    # For players with abreviated names
    name = ''.join(name.split("."))
    
    # need to separate the Jabar part so we initialize the first part of the split
    name = (name.split("-"))[0]
    fullName = name.split(" ")
    return fullName


# uses a list first, last to build the url to look up specific player.
def BuildPlayerURL(name):
    tempURL = 'https://www.basketball-reference.com/players/'
    tempURL += name[-1][0].lower() + '/'
    if len(name[-1]) > 5:
        tempURL += (name[-1][:5] + name[0][:2]).lower() + '01.html'
    else:
        tempURL += (name[-1] + name[0][:2]).lower() + '01.html'
    return tempURL

# Ensuring the name matches the name provided
def EnsureUrlIsCorrect(builtURL, tempName):
    tempPlayer = Player()
    html_text = requests.get(builtURL).text
    soup = BeautifulSoup(html_text, 'lxml')
    pageTitle = soup.find("div", {"id" : "meta"})
    pageName = pageTitle.find("span").get_text()
    if pageName == tempName:
        tempPlayer = FindPlayerSpecificData(html_text, tempName)
    else:
        numberOfNamesPage = int(builtURL[-6])
        # increments the digit by 1
        builtURL = str(numberOfNamesPage+1).join(builtURL.split(str(numberOfNamesPage)))
        EnsureUrlIsCorrect(builtURL, tempName)

    return tempPlayer