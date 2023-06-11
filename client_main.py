import grpc
import signal
import os
import sys
import time
import asyncio
from random import randint

import mafia_pb2
import mafia_pb2_grpc
import grpc
stub = None

from pprint import pprint
import time
from sys import argv

BOT = 'bot'
HUMAN = 'human'
# Default Server Address For Testing
host = '127.0.0.1'  # Или 'localhost'
port = '5000'


ROLE_UNKNOWN = 'Unknown'
ROLE_INNOCENT = 'Innocent'
ROLE_COMMISSAR = 'Commissar'
ROLE_MAFIOSI = 'Mafia'
ROLE_DEAD = 'Dead'
DAY = "Day"
NIGHT = "Night"

IN_PREPARATION = 0
ONGOING = 1
INVALID = 2


class MafiaClient:
    def __init__(self, stub, channel):
        super().__init__() # just in case
        self.stub = stub
        self.channel = channel
        self.username = None
        self.room_name = None
        self.role = None
        self.status = None
        self.players = dict()
        self.names = list()
        self.iteration = 0
        self.unknown_roles = list() # for comissar role

    
    async def send_message(self, content):
        print("...")

        response = await self.stub.SendMessage(
            mafia_pb2.SendMessageRequest(username=self.username, room_name=self.room_name, content=content))
        
        if not response.flag:
            self.room_name = None
        print(response.message)
        return response.flag
    

    async def choose_mode(self, word):
        if word == '' or word == '\n':
            while word == '' or word == '\n':
                word = input("Wrong format. Do you want to enter existing room? [y/n] ")
        if word[0] == 'y':
            word = 'join'
        else:
            word = 'create'
        return word


    async def create_room(self):
        print("connecting...")

        response = await self.stub.CreateRoom(
            mafia_pb2.CreateRoomRequest(username=self.username, room_name=self.room_name))
        
        if not response.flag:
            self.room_name = None
        print(response.message)
        return response.flag


    async def join_room(self):
        response = await self.stub.JoinRoom(
            mafia_pb2.JoinRoomRequest(room_name=self.room_name, username=self.username)
        )
        if not response.flag:
            print(response.message)
            return False

        return True


    async def start(self):
        self.username = input("Identify yourself: ")

        while True:
            mode = input("Do you want to enter existing room? [y/n] ")
            mode = await self.choose_mode(mode)
            self.room_name = input("Enter room name: ")

            if mode == 'join':
                print("Wait for a bit...")

                if not await self.join_room():
                    print("Something's off \n")
                    continue
                break

            if mode == 'create':
                print("Creating. Wait for a bit...")
                if not await self.create_room():
                    print("Something's off... \n")
                    continue
                print(f"Room {self.room_name} created! Waiting everyone to join... \n ")
                if not await self.join_room():
                    print("Something's off... \n")
                    continue
                print(f"Room {self.room_name} created and joined! Begin! \n ")
                break
        
        response = await self.stub.GetPlayers(mafia_pb2.GetPlayersRequest(room_name=self.room_name))
        print(response.names)
        for i in range(len(response.names)):
            self.players[response.names[i]] = response.roles[i]

        self.names = response.names[:]
        self.status = True
        self.role = self.players[self.username]
        self.unknown_roles = response.names[:]
        self.unknown_roles.remove(self.username)
        print('Roles were assigned! \n')
        
    
    #GAME HELPERS
    async def get_player_info(self):
        response = await self.stub.GetRole(
            mafia_pb2.GetRoleRequest(username=self.username, room_name=self.room_name))
        
        return response
        

    async def get_day_victim(self, vote):
        if vote == None:
            vote = ''
        
        response = await self.stub.VotePaper(mafia_pb2.VotePaperRequest(room_name=self.room_name, victim=vote, username=self.username))
        response = await self.stub.DayToNight(mafia_pb2.DayToNightRequest(room_name=self.room_name, username=self.username))
        return response
        

    async def get_night_victim(self, vote):
        if self.role != ROLE_MAFIOSI or self.status != True:
            vote = ''
        if vote == None:
            vote = ''
        response = await self.stub.VotePaper(mafia_pb2.VotePaperRequest(room_name=self.room_name, victim=vote, username=self.username))
        response = await self.stub.NightToDay(mafia_pb2.NightToDayRequest(room_name=self.room_name, username=self.username, victim=vote))
        return response
    

    async def handle_death(self, victim):
        if victim == '':
            print('No one died!')
            return

        if self.username == victim:
            print('Sorry, you were killed this night, no luck \n')
            self.status = False
            self.role = ROLE_DEAD
        else:
            print('Still alive and kicking! Congrats \n')
            print(f'Player {victim} was murdered... F')
        self.players[victim] = ROLE_DEAD
        return
        


async def handle_requests(client, mode):
    if mode == BOT :
        return
    
    while True:
        print("Anything you want to know? Here are your options: \n ")
        print("1. Remind me my role \n2. How many players still alive? \n3. Show me players names \n4. No, proceed \n")
        question = input("Please, write a number of one of the options above: ")

        if question == '' or question == '\n':
            while question == '' or question == '\n':
                question = input("Please, write a number of one of the options above: ")

        if question[0] == '1':
            print(f'You are playing as {client.role} \n')
            continue
        elif question[0] == '2':
            for key, val in client.players.items():
                if val != ROLE_DEAD:
                    print(f'{key} ')
            continue
        elif question[0] == '3':
            for key, val in client.players.items():
                if val != ROLE_DEAD:
                    print(f'{key} ')
                else:
                    print(f'{key} [DEAD]')
            continue
        elif question[0] == '4':
            print('Ok, proceeding...')
        break  


async def day_vote_handler(client, mode):
    vote_list = []
    vote = None
    if mode == BOT:
        if client.status:
            for key, value in client.players.items():
                if key != client.username and value != ROLE_DEAD:
                    vote_list.append(key)

            vote = vote_list[randint(0, len(vote_list) - 1)]

    else:
        if client.status:
            vote = input("Who are you voting for: ")
            while True:
                if vote not in client.names:
                    vote = input("No idea who that is. Who are you voting for: ")
                    continue
                if vote == client.username or client.players[vote] == ROLE_DEAD:
                    vote = input("No voting for yourself or dead. Who are you voting for: ")
                    continue
                break
    return vote


async def night_vote_handler(client, mode):
    vote_list = []
    vote = None
    check = None
    if mode == BOT:
        if client.status:
            if client.role == ROLE_MAFIOSI:
                for key, value in client.players.items():
                    if value != client.role and key != client.username:
                        vote_list.append(key)

                vote = vote_list[randint(0, len(vote_list) - 1)]

    else:
        if client.status:
            if client.role == ROLE_MAFIOSI:
                vote = input("Write who are you voting for: ")
                while True:
                    if vote not in client.names:
                        vote = input("No idea who that is. Who are you voting for: ")
                        continue
                    if vote == client.username or client.players[vote] == ROLE_DEAD:
                        vote = input("No voting for yourself or dead. Who are you voting for: ")
                        continue
                    break
 
            if client.role == ROLE_COMMISSAR:
                check = input("Who are you checking: ")
                while check not in client.names:
                    check = input("No idea who that is. Who are you checking: ")
                print(f"Player {check} actually is {client.players[check]} !")      
    return vote


            
async def mafia_game_function(client):
    print('Welcome to SoaMafiaGame! Lets begin :) \n')
    await client.start()

    print(f'This time you are... {client.role}\n')

    first_day = True

    mode = input("Do you want to enter bot mode? [y/n] ")

    if mode == '' or mode == '\n':
        while mode == '' or mode == '\n':
            mode = input("Wrong format. Do you want to enter bot mode? [y/n] ")
    if mode[0] == 'y' or mode[0] == 'Y':
        mode = BOT
        print('You are playing as a bot now!n \n ')
    else:
        mode = HUMAN
        print('Ok, choose wisely \n')

    while True:
        day_vote = None
        night_vote = None
        client.iteration += 1
        print(f'This is day numer {client.iteration}! \n')
        if client.status:
            if  first_day:
                await handle_requests(client, mode)
                print(f'No voting today... \n')
            else:
                print(f'It is time for daily voting... Let us hope you survive :) \n')
                day_vote = await day_vote_handler(client, mode)
                print(f'You made your choice \n')
        else:
            print(f'Sorry, you are dead now... Waiting for results announcement... \n')
        
        if not first_day:
            print(f'Waiting for all player to join day voting \n')
            response = await client.get_day_victim(day_vote)
            print(f'Vote completed! \n')
            await client.handle_death(response.victim)
            if response.flag:
                print(response.message)
                break
        else:
            first_day = False

        
        # DAILY VOTE RESULS!!!!!!!!!!!!!!

        print('City falls asleep, now wait a bit... \n')
        if client.status:
            night_vote = await night_vote_handler(client, mode)
        else:
            print(f'Sorry, you are dead now... Waiting for results announcement... \n')
        
        print(f'Waiting for all player to join night voting \n')
        response = await client.get_night_victim(night_vote)
        print(f'Vote completed! \n')
        await client.handle_death(response.victim)
        if response.flag:
            print(response.message)
            break
        # NIGHT VOTE RESULTSSSSS!!!!!!!!!!!!

    print('Restart program if you wanna play again! ')
    return




async def run() -> None:
    try:
        channel = grpc.aio.insecure_channel(f'{host}:{port}')
        stub = mafia_pb2_grpc.MafiaStub(channel)

        game_client = MafiaClient(stub, channel)

        # main logic
        await asyncio.gather(
            mafia_game_function(game_client)
        )
    except SystemExit:
        pass


if __name__ == '__main__':
    asyncio.run(run())
