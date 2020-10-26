import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import *

# Google Sheets FrameWork

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheets1 = client.open(googleSheetsName).sheet1


def getCurrentLines(position):
    if position == 2:
        ExpenseCurrentLines = sheets1.acell("U2").value
        return ExpenseCurrentLines
    elif position == 3:
        IncomeCurrentLines = sheets1.acell("U3").value
        return IncomeCurrentLines
    elif position == 4:
        NameCurrentLines = sheets1.acell("U4").value
        return NameCurrentLines


def updateCurrentLines(line, position):
    cell = "U" + str(position)

    sheets1.update(cell, str(int(line) + 1))


# msgList is the list of our Name,Price,PaymentType,Category
# rowNumber will be our current row of unCategorizedItems

def inputUnCategorizedItem(msgList, rowNumber):
    for i in range(len(msgList)):
        sheets1.update_cell(rowNumber, i + 1, msgList[i])
    print(f"inputted {msgList}")


def resetCurrentLine(position):
    cell = "U" + str(position)
    sheets1.update(cell, "2")


def clearWeek():
    emptyCells = ["", "", "", "", ""]
    newCell = []
    numOfRows = int(sheets1.row_count)
    for i in range(numOfRows - 1):
        newCell.append(emptyCells)
    sheets1.update("A2:E", newCell)
    resetCurrentLine(ExpensePosition)


def addIncome(msgList, rowNumber):
    for i in range(len(msgList)):
        sheets1.update_cell(rowNumber, i + 7, msgList[i])
    print(f"inputted {msgList}")


def getDataFromSheets(cellStart, cellEnd):
    cell = cellStart + ':' + cellEnd
    sheets = sheets1.get(cell)
    return sheets


def getDataFromCell(cell):
    return sheets1.get(str(cell))


def addNumberToGSheets(name, number):
    NameCurrentLines = getCurrentLines(NamePosition)
    ColY = "Y" + str(NameCurrentLines)
    ColZ = "Z" + str(NameCurrentLines)
    sheets1.update(ColY, name)
    sheets1.update(ColZ, number)
    updateCurrentLines(NameCurrentLines, 4)
