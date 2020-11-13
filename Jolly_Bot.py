# bot.py
import os
import random
import discord
import re
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
user1 = "none"
user2 = "none"
challengeCheck = 0
memCheck = 0


class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    client = discord.Client(intents=intents)



@client.event            #Welcoming message for new users joining the server
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )




@client.event #message event
async def on_message(message):
    global user1
    global user2
    global challengeCheck
    global memCheck

    if message.author == client.user:
        return
    if re.search('^,r', message.content):  # This is a challenge in progress check
        if challengeCheck == 1:
            await message.channel.send("There is already a challenge pending you heathen!")
            return

        user1 = message.author.name
        user2 = message.content.split(" ", 1)[1]
        print ("user 1: " + user1 + " user 2: " + user2)
        if user1 == user2:                      # This is to make sure you can't play against yourself
            await message.channel.send("Oh no you don't go spill your brains some place else...")
            return
        for member in message.guild.members:
            print(member.display_name)
            if user2 == member.display_name:
                response = f"{user1} has challenged {user2} to a game of russian roulette! Will {user2} step up to {user1} bravado?!?!"
                await message.channel.send(response)
                challengeCheck = 1
                return
        else:                                    # This catches if a user does not exist
            await message.channel.send("That user isn't on the server!")

    elif re.search('^,accept', message.content) and challengeCheck == 1:
        bullet = 1
        players = ["none"] * 2
        playerIndex = 1
        cylinder = [0] * 6 
        players[0] = user1 #load the players
        players[1] = user2
        bulletIndex = random.randint(0, 5) #Create a random place to put the bullet
        cylinder[bulletIndex] = 1 #Load the bullet
        currentCylinder = random.randint(0, 5) #spin the cylinder

        while bullet == 1:

            randomTime = random.randint(2, 7)
            await message.channel.send(f"{players[playerIndex]} picks up the gun, brings it to their head and...")
            time.sleep(randomTime)
            print("its looping")
            if cylinder[currentCylinder] == 1:
                print("blammo")
                await message.channel.send(f"BLAMMO!! {players[playerIndex]} falls to the floor lifeless...")
                bullet == 0
                cylinder.pop()
                challengeCheck = 0
                return "blammo"
            else:
                print("click")
                await message.channel.send("CLICK!!")
                await message.channel.send(f"{players[playerIndex]} sweats profusely and drops the gun on the table")
                time.sleep(2)
                if currentCylinder == 5:
                    currentCylinder = 0
                else:
                    currentCylinder += 1
                if playerIndex == 1:
                    playerIndex = 0
                else:
                    playerIndex += 1

    elif re.search('^,accept', message.content) and challengeCheck == 0:    #Checks for active challenge
        await message.channel.send("There are no challenges at this time...")
    elif re.search('^,cancel', message.content):                            #Cancels the challenge
        await message.channel.send(f"{user1} has cancelled the challenge")
        challengeCheck = 0
    elif re.search('^,help', message.content) or re.search('^,', message.content):  #The help request
        await message.channel.send("Challenge someone with ,r or accept a challenge with ,accept")




client.run(TOKEN)
