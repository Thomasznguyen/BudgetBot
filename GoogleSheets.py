import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import *

# Google Sheets FrameWork

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheets = client.open(googleSheetsName).sheet1


# msgList is the list of our Name,Price,PaymentType,Category
# rowNumber will be our current row of unCategorizedItems

def inputUnCategorizedItem(msgList, rowNumber):
    for i in range(len(msgList)):
        if i == 1:
            sheets.update_cell(rowNumber, i + 1, (msgList[1]))
        else:
            sheets.update_cell(rowNumber, i + 1, msgList[i])
    print(f"inputted {msgList}")


def clearWeek():
    emptyCells = ["", "", "", "", ""]
    newCell = []
    numOfRows = int(sheets.row_count)
    for i in range(numOfRows - 1):
        newCell.append(emptyCells)
    sheets.update("A2:E", newCell)


def getDataFromSheets():
    cellStart = "A2"
    cellEnd = "E"
    cell = cellStart + ':' + cellEnd
    return sheets.get(cell)


def getDataFromCell(cell):
    return sheets.get(str(cell))
