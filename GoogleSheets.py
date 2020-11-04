import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import *

# Google Sheets FrameWork

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

googleSheets = client.open(googleSheetsName)

sheets1 = googleSheets.get_worksheet(0)
sheets2 = googleSheets.get_worksheet(1)


def getCurrentLines(position):
    CellPos = "X" + str(position)
    LoginCurrentLine = sheets1.acell(CellPos).value
    return LoginCurrentLine


def updateCurrentLines(line, position):
    cell = "X" + str(position)
    sheets1.update(cell, str(int(line) + 1))


def resetCurrentLine(position):
    cell = "X" + str(position)
    sheets1.update(cell, "2")


def addMessages(msgList):
    MessageCurrentLines = getCurrentLines(IncomingMesPosition)
    numberCol = "M" + str(MessageCurrentLines)
    bodyCol = "N" + str(MessageCurrentLines)
    DateCol = "O" + str(MessageCurrentLines)
    sheets1.update(numberCol, msgList[0])
    sheets1.update(bodyCol, msgList[1])
    sheets1.update(DateCol, msgList[2])
    updateCurrentLines(MessageCurrentLines, IncomingMesPosition)

def sentMessageLogs(number,message):
    MessageCurrentLines = getCurrentLines(OutMessagePosition)
    NameCol = "R" + str(MessageCurrentLines)
    messageCol = "S" + str(MessageCurrentLines)
    sheets1.update(NameCol, number)
    sheets1.update(messageCol, message)
    updateCurrentLines(MessageCurrentLines,OutMessagePosition)



def addLogin(username, password):
    LoginCurrentLines = getCurrentLines(LoginPosition)
    usernameCol = "C" + str(LoginCurrentLines)
    passwordCol = "D" + str(LoginCurrentLines)
    accessCol = "E" + str(LoginCurrentLines)
    sheets1.update(usernameCol, username)
    sheets1.update(passwordCol, password)
    sheets1.update(accessCol, "user")
    updateCurrentLines(LoginCurrentLines, LoginPosition)


def searchLogin(username,password):
    loginData = getDataFromSheets(LOGINCELLSTART, LOGINCELLEND)
    # code for knownPerson:
    # False = no person is in DataBase
    # True = username and password Matches
    # -1 = only username is found
    print(loginData)
    for i in range(len(loginData)):
        if username in loginData[i]:
            if password in loginData[i]:
                if "admin" in loginData[i]:
                    return "admin"
                return True
            else:
                return -1
    return False


def getDataFromSheets(cellStart, cellEnd):
    cell = cellStart + ':' + cellEnd
    sheets = sheets1.get(cell)
    return sheets


def getDataFromCell(cell):
    return sheets1.get(str(cell))


def checkalreadyin(name, number):
    numberData = getDataFromSheets(CellPhoneCellStart, CellPhoneCellEnd)
    for i in range(len(numberData)):
        if number in numberData[i]:
            return "foundnumber"
        if name in numberData[i]:
            return "foundname"
    return False


def findNumber(name):
    numberData = getDataFromSheets(CellPhoneCellStart, CellPhoneCellEnd)
    personNumber = -1
    for i in range(len(numberData)):
        if name in numberData[i]:
            personNumber = numberData[i][1]
            i = len(numberData)
    return personNumber


def findName(number):
    numberData = getDataFromSheets(CellPhoneCellStart, CellPhoneCellEnd)
    personName = -1
    for i in range(len(numberData)):
        if number in numberData[i]:
            personName = numberData[i][0]
            i = len(numberData)
    return personName


def addNumberToGSheets(name, number):
    NameCurrentLines = getCurrentLines(NamePosition)
    ColY = "Z" + str(NameCurrentLines)
    ColZ = "AA" + str(NameCurrentLines)
    sheets1.update(ColY, name)
    sheets1.update(ColZ, number)
    updateCurrentLines(NameCurrentLines, NamePosition)
