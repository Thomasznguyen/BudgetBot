# BudgetBot
This is a small little budget bot using gspread and discord to help you keep track of your expense from your phone
This program needs to first be setted up with google's api which you can download: https://developers.google.com/sheets/api/quickstart/python 
This program will also need to setup a discord bot at: https://discord.com/developers/applications


Using Discord's python api for the user interaction with google's gspread api for a rough database to store our budget information
The discord Bot is kept alive 24/7 using Heroku's Hobby Dyno which is used to take in user's input

The !budget command will allow the user to enter in a new expense
!getcat (!cat) will allow the user to get the data from a specific category
!gettotal will allow the user to get the total expenditure
!getcattotal or (!catt) will allow the user to get the total expenditure from a specific category

