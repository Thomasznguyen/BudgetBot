import gspread
from oauth2client.service_account import ServiceAccountCredentials
from GoogleSheets import *
import discord
from discord.ext import commands
from config import *
from datetime import date

global currentLines

bot = commands.Bot(command_prefix=PREFIX, description="!help for list of commands")


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
        global currentLines
        inputUnCategorizedItem(msgList, currentLines)
        # increase the row we are on.
        currentLines += 1

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
    sentMsg = f"Name: **{data[0]}** | Price: **{data[1]}** | " \
              f"PaymentMethod: **{data[2]}** | Category: **{data[3]}** | " \
              f"Date: **{data[4]}**"
    return sentMsg


"""
This function will get all the inputted data out of the google sheets
:parameter None
:return Formatted printed list.
"""


@bot.command(pass_context=True, aliases=['get'])
async def getdata(ctx):
    data = getDataFromSheets()
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

Current runs at O(n^2) could get it to be better!!!!
"""


@bot.command(pass_context=True, aliases=['cat'])
async def getcat(ctx, category):
    # Extracting Data from googleSheets
    data = getDataFromSheets()
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
    data = getDataFromSheets()
    totalPrice = 0
    for i in range(len(data)):
        totalPrice += float(data[i][1])
    await ctx.send(f"You spent ${totalPrice} this week")


@bot.command(pass_context=True, aliases=['cattotal', 'catt'])
async def getcattotal(ctx, category):
    data = getDataFromSheets()
    totalPrice = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == category:
                totalPrice += float(data[i][1])
    await ctx.send(f"You spent a total of ${totalPrice} in {category}")


@bot.command(pass_context=True, aliases=['clearWeek'])
async def newWeek(ctx):
    clearWeek();
    await ctx.send(f"Week of {date.today()} cleared")
    global currentLines
    currentLines = 2


bot.run(TOKEN, bot=True, reconnect=True)
