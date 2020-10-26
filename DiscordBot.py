import gspread
from oauth2client.service_account import ServiceAccountCredentials
from GoogleSheets import *
import discord
from discord.ext import commands
from config import *
from datetime import date
from textClient import *

bot = commands.Bot(command_prefix=PREFIX, description="!help for list of commands")


# This is a de-bug and Log command that will send out a message whenever a bot comes online

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and connected to Discord! (ID: {bot.user.id})")
    game = discord.Game(name="!help for list of commands")
    await bot.change_presence(activity=game)


"""
This Command will allow us to enter in items 
to be store in our google sheets database
we can then perform a wide range of function on
that database such as getting back remaining budget on a
specific category etc... etcc
"""


@bot.command(pass_context=True, aliases=['b'])
async def budget(ctx):
    parameters = 5
    await ctx.send("Please enter your items FORMAT[name,price,payment type, category] (STOP to stop)")

    def check(msg):
        return msg.author == ctx.author

    # We are getting in the item we bought in the following format
    # Name of Item = 1
    # Amount spent = 2
    # Type of payment (cash,credit,debit) = 3
    # category = 4
    today = str(date.today())
    msg = await bot.wait_for('message', check=check)
    msgContent = msg.content
    msgList = msgContent.lower().split()
    msgList.append(today)
    while "stop" not in msgList:
        # For this version of our code we require 4 specific category
        # this while loop should keep asking for the msg
        while (len(msgList) != parameters):
            await ctx.send("Please enter your items FORMAT[name,price,payment type, category] (STOP to stop)")
            msg = await bot.wait_for('message', check=check)
            msgContent = msg.content
            msgList = msgContent.lower().split()
            msgList.append(today)
            # if it reaches the sentinel value break out,
            if "stop" in msgList:
                break

        # We will now try to input this item into the google sheet
        ExpensecurrentLines = getCurrentLines(ExpensePosition)
        inputUnCategorizedItem(msgList, ExpensecurrentLines)
        # increase the row we are on.
        updateCurrentLines(ExpensecurrentLines, ExpensePosition)
        # Repeat loop.
        await ctx.send("Please enter your items \n FORMAT[name,price,payment type, category] (STOP to stop)")
        msg = await bot.wait_for('message', check=check)
        msgContent = msg.content
        msgList = msgContent.lower().split()
        msgList.append(today)


@bot.command(pass_context=True, aliases=['income', 'money'])
async def addmoney(ctx):
    parameters = 4
    await ctx.send("Please enter your Income \n FORMAT[IncomeName,Amount,IncomeMethod] (STOP to stop)")

    def check(msg):
        return msg.author == ctx.author

    # We are getting in the item we bought in the following format
    # Name of Income = 1
    # Income Amount = 2
    # Type of Income = 3
    today = str(date.today())
    msg = await bot.wait_for('message', check=check)
    msgContent = msg.content
    msgList = msgContent.lower().split()
    msgList.append(today)
    while "stop" not in msgList:
        # For this version of our code we require 4 specific category
        # this while loop should keep asking for the msg
        while (len(msgList) != parameters):
            await ctx.send("Please enter your items FORMAT[name,price,payment type, category] (STOP to stop)")
            msg = await bot.wait_for('message', check=check)
            msgContent = msg.content
            msgList = msgContent.lower().split()
            msgList.append(today)
            # if it reaches the sentinel value break out,
            if "stop" in msgList:
                break

        # We will now try to input this item into the google sheet
        IncomeCurrentLines = getCurrentLines(IncomePosition)
        addIncome(msgList, IncomeCurrentLines)
        # increase the row we are on.
        updateCurrentLines(IncomeCurrentLines, IncomePosition)
        # Repeat loop.
        await ctx.send("Please enter your items FORMAT[name,price,payment type, category] (STOP to stop)")
        msg = await bot.wait_for('message', check=check)
        msgContent = msg.content
        msgList = msgContent.lower().split()
        msgList.append(today)


"""
This function will return a formatted print statement
that will tell the user all the information
:parameters: data, a list of data about a specific item.
"""


def format_output(data):
    sentMsg = f"{data[0]:10} | {data[1]:>20}  | " \
              f"{data[2]:>10} | {data[3]:>20} | " \
              f"{data[4]:>20}"
    return sentMsg


"""
This function will get all the inputted data out of the google sheets
:parameter None
:return Formatted printed list.
"""


@bot.command(pass_context=True, aliases=['get'])
async def getdata(ctx):
    data = getDataFromSheets(ExpenseCellStart, ExpenseCellEnd)
    # search through the data and prints out that information
    for i in range(len(data)):
        if (data[i]):
            msg = format_output(data[i])
            await ctx.send(msg)


"""
This command will get any data that is inside a specific 
category such as paymentMethod of cash, it'll get all cash payment
It will also work with getting spending category.

:parameter category: a specific category to search the google
sheets for.
:return: a formatted output of all purchases

"""


@bot.command(pass_context=True, aliases=['cat'])
async def getcat(ctx, category):
    # Extracting Data from googleSheets
    data = getDataFromSheets(ExpenseCellStart, ExpenseCellEnd)
    # This loop will look for the category
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == category:
                msg = format_output(data[i])
                await ctx.send(msg)


"""
This command will get a cell from the googleSheet that
has the total expenditure of this week:
"""


@bot.command(pass_context=True, aliases=['total'])
async def gettotal(ctx):
    # Extracting Data from googleSheets
    data = getDataFromSheets(ExpenseCellStart, ExpenseCellEnd)
    totalPrice = 0
    print(data)
    for i in range(len(data)):
        if i != 0:
            price = float(data[i][1])
            totalPrice += price
    await ctx.send(f"You spent ${totalPrice} this week")


@bot.command(pass_context=True, aliases=['cattotal', 'catt'])
async def getcattotal(ctx, category):
    data = getDataFromSheets(ExpenseCellStart, ExpenseCellEnd)
    totalPrice = 0.0
    for i in range(len(data)):
        for j in range(len(data[i])):
            # Searches through the data and looks to see if it matches the cat
            if data[i][j] == category:
                if i != 0:
                    price = float(data[i][1])
                    totalPrice += price
    await ctx.send(f"You spent a total of ${totalPrice} in {category}")


# this command will clearOut the expenses and reset our current position

@bot.command(pass_context=True, aliases=['clearWeek'])
async def newWeek(ctx):
    clearWeek();
    await ctx.send(f"Week of {date.today()} cleared")


# This section of code deals with sending SMS message through discord commands
"""
format_sms_output()
:parameter: This is our data at a given row
:return: a formatted string that looks for SMS
"""


def format_sms_output(data):
    sentMsg = (f"Expense Name: {data[0]} \n"
               f"Price: {data[1]} \n"
               f"Payment Method: {data[2]} \n"
               f"Category: {data[3]} \n"
               f"Date: {data[4]} \n"
               f"-------------\n")
    return sentMsg


"""
This number will first check the user to see if they're in the database
if they're not then it will try to add them
It will then send a formatted message to the given phoneNumber

:parameter: info is either the user's name or phoneNumber
"""


# needs Documentation
@bot.command(pass_context=True, aliases=['gsms'])
async def getsms(ctx, info):
    numberData = getDataFromSheets(CellPhoneCellStart, CellPhoneCellEnd)
    knowNumber = False
    personNumber = 0

    def check(msg):
        return msg.author == ctx.author

    for i in range(len(numberData)):
        if info in numberData[i][0]:
            knowNumber = True
            personNumber = numberData[i][1]
            i = len(numberData)
    if not knowNumber:
        await ctx.send(f"{info} is not in our database would you like to add it?")
        addNum = await bot.wait_for('message', check=check)
        if "yes" in str(addNum.content).lower():
            await ctx.send(f"What name would you like to assign {info}")
            addName = await bot.wait_for('message', check=check)
            name = str(addName.content)
            addNumberToGSheets(name, info)
            await ctx.send(f"Added {info} to {addName.content}")
        else:
            await ctx.send("Okay! it would be easier next time to add it to our DataBase")

    else:
        await ctx.send(f"Ahh {info} it seems you are already "
                       f"in our database through the number {personNumber}")

    data = getDataFromSheets(ExpenseCellStart, ExpenseCellEnd)
    combinedMSG = ""
    for i in range(len(data)):
        if (data[i]):
            if i != 0:
                msg = format_sms_output(data[i])
                combinedMSG = combinedMSG + str(msg)
    if not knowNumber:
        sendSMS(info, combinedMSG)
        print(f"sent {addName.content} {combinedMSG}")
    else:
        sendSMS(info, combinedMSG)
        print(f"sent {info} \"{combinedMSG}\"")


@bot.command(pass_context=True, aliases=['textPerson'])
async def text(ctx, number, message):
    numberData = getDataFromSheets(CellPhoneCellStart, CellPhoneCellEnd)
    knowNumber = False
    personNumber = 0

    def check(msg):
        return msg.author == ctx.author

    for i in range(len(numberData)):
        if number in numberData[i][0]:
            knowNumber = True
            personNumber = numberData[i][1]
            i = len(numberData)
    if not knowNumber:
        await ctx.send(f"{number} is not in our database would you like to add it?")
        addNum = await bot.wait_for('message', check=check)
        if "yes" in str(addNum.content).lower():
            await ctx.send(f"What name would you like to assign {number}")
            addName = await bot.wait_for('message', check=check)
            name = str(addName.content)
            addNumberToGSheets(name, number)
            await ctx.send(f"Added {number} to {addName.content}")
        else:
            await ctx.send("Okay! it would be easier next time to add it to our DataBase")

    else:
        await ctx.send(f"Ahh **{number}** it seems you are already "
                       f"in our database through the number {personNumber}")
    if not knowNumber:
        sendSMS(number, message)
        print(f"sent {addName.content} {message}")
    else:
        sendSMS(personNumber, message)
        print(f"sent {personNumber} \"{message}\"")


@bot.command(pass_context=True, aliases=['anum'])
async def addnum(name, number):
    addNumberToGSheets(name, number)
    print(f"Added {number} to {name}")


bot.run(TOKEN, bot=True, reconnect=True)
