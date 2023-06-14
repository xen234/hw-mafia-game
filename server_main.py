from concurrent import futures
import random
import os
import asyncio
## pip modules
import grpc
# import rich.traceback # for logs
# import rich.console
## proto3 generated code
import mafia_pb2
import mafia_pb2_grpc
import grpc
from collections import defaultdict

## homemade code

host = '0.0.0.0'  # Или 'localhost'
port = '50051'


ROLE_UNKNOWN = 'Unknown'
ROLE_INNOCENT = 'Innocent'
ROLE_COMMISSAR = 'Commissar'
ROLE_MAFIOSI = 'Mafia'
ROLE_DEAD = 'Dead'
DAY = "Day"
NIGHT = "Night"

# rich_out_con = rich.console.Console()
roles = [ROLE_COMMISSAR, ROLE_MAFIOSI, ROLE_INNOCENT, ROLE_INNOCENT]
IN_PREPARATION = 'Preparing'
ONGOING = 'Game In Session'
OVER = 'Game over'
WIN_MAFIA = 'Mafia won!'
WIN_INNOCENT = 'Innocent won!'


class Member:
    _counter = 0

    def __init__(self, nickname):
        self.username = nickname
        self.status = True
        self.role = None

    

class MafiaRoom:
    def __init__(self, room_name, username):
        self.sync_point = asyncio.Condition()
        self.sync_counter = 0
        self.room_name = room_name
        self.host = username
        
        self.players = list() # stores names
        self.round_num = 0
        self.killed=''
        self.waiting=0

        self.room_status = IN_PREPARATION
        self.alive_number = 4
        self.statuses = dict() # name : status
        self.assigned_roles = dict() # name : role
        self.masked_roles = dict() # name : masked role
        self.vote_paper = defaultdict(int) # name: vote

        self.chat = list() # SendMessageResponses
        self.system_messages = list() # ActionResponses

        self.info = list()


class MafiaServicer(mafia_pb2_grpc.MafiaServicer):
    def __init__(self):
        super().__init__() # just in case

        self.rooms = dict()
        self.room_names = list()

        print("Server started. Waiting for players.")

    
    async def ChatStream(self, request, context):
        chat_iter = 0
        while True:
            if chat_iter >= len(self.rooms[request.room_name].chat):
                await asyncio.sleep(0)
                continue
            yield self.rooms[request.room_name].chat[chat_iter]
            if self.rooms[request.room_name].chat[chat_iter].flag:
                # ok message
                print(f"Message in room {request.room_name} from {self.rooms[request.room_name].chat[chat_iter].username} : \n \
                       {self.rooms[request.room_name].chat[chat_iter].content}")
            else:
                # warning 
                print(f"Message error in {request.room_name}: {self.rooms[request.room_name].chat[chat_iter].warning}")
            chat_iter += 1


    async def Action(self, request, context):
        message_iter = 0
        while True:
            if message_iter >= len(self.rooms[request.room_name].system_messages):
                await asyncio.sleep(0)
                continue
            yield self.rooms[request.room_name].system_messages[message_iter]
            print(f"Next: {self.rooms[request.room_name].system_messages[message_iter].message}")
            if self.rooms[request.room_name].room_status == OVER:
                await asyncio.sleep(0)
                keys_to_delete = []
                for key, value in self.rooms.items():
                    if value == request.room_name:
                        keys_to_delete.append(key)

                for key in keys_to_delete:
                    del self.rooms[key]
            message_iter += 1

    
    def SendMessage(self, request, context):
        # checking if valid
        if request.content == '':
            response = mafia_pb2.SendMessageResponse(flag=False, username=request.username, content='', warning="No message to deliver. \n")
        elif request.room_name not in self.room_names:
            response = mafia_pb2.SendMessageResponse(flag=False, username=request.username, content='', warning="No such room found. \n")
        elif self.rooms[request.room_name].room_status != ONGOING:
            response = mafia_pb2.SendMessageResponse(flag=False, username=request.username, content='', warning="Room is not avaliable. \n")
        elif len(request.content) >= 500:
            response = mafia_pb2.SendMessageResponse(flag=False, username=request.username, content='', warning="Message is too long. \n")
        else:
            # adding to chat queue
            response = mafia_pb2.SendMessageResponse(flag=True, username=request.username, content=request.content)
        
        self.rooms[request.room_name].chat.append(response)
        
        return response


    async def CreateRoom(self, request, context):
        # checking if valid
        print('adding')
        if request.room_name in self.room_names:
            return mafia_pb2.CreateRoomResponse(flag=False, message="Oops, name taken! \n")
        elif request.room_name == '':
            return mafia_pb2.CreateRoomResponse(flag=False, message="Invalid room name \n")
        
        # creating room
        self.rooms[request.room_name] = MafiaRoom(request.room_name, request.username)
        self.room_names.append(request.room_name)

        print(f"Room {request.room_name} created")

        self.rooms[request.room_name].system_messages.append(
            mafia_pb2.ActionResponse(flag=True, message=f"You've created the {request.room_name} room \n")
        )

        return mafia_pb2.CreateRoomResponse(flag=True, message=f"Room {request.room_name} was successfully created! \n")
            
    
    #helper_function
    def assign_roles(self, room):
        assigned = random.shuffle(roles.copy())
        i = 0
        for player in room.players:
            room.assigned_roles[player] = assigned[i]
            room.statuses[player] = True
            room.masked_roles[player] = ROLE_UNKNOWN
            i += 1 
        print("Roles assigned!")
        return room

 
    async def JoinRoom(self, request, context):
        # checking if valid 
        if request.room_name not in self.room_names:
            return mafia_pb2.JoinRoomResponse(flag=False, message="No such room found. Please, create one first \n")

        for player in self.rooms[request.room_name].players:
            if player == request.username:
                return mafia_pb2.JoinRoomResponse(flag=False, message="Name taken\n")
        
        #adding to queue 
        print(f"Adding player {request.username}.")
        cur = self.rooms[request.room_name]

        if len(cur.players) <= 3:
            self.rooms[request.room_name].players.append(request.username)
            self.rooms[request.room_name].system_messages.append(mafia_pb2.ActionResponse(flag=True, 
                                                                message=f"Player {request.username} is waiting to join the room... "))     
        else:
            self.raise_internal_error("TOO_MANY_PLAYERS", context)
            return mafia_pb2.JoinRoomResponse(flag=False, message="Too many players\n")
        
        # start if enough players 
        if len(cur.players) >= 4:
            async with self.rooms[request.room_name].sync_point:
                assigned = roles.copy()
                random.shuffle(assigned)
                i = 0
                for player in self.rooms[request.room_name].players:
                    self.rooms[request.room_name].assigned_roles[player] = assigned[i]
                    print(f'{request.username} MADE roles')
                    self.rooms[request.room_name].statuses[player] = True
                    print(f'{request.username} MADE Statuses')
                    self.rooms[request.room_name].masked_roles[player] = ROLE_UNKNOWN
                    print(f'{request.username} MADE mask')
                    i += 1 
                    print(f'{request.username} MADE finished')
                print("Roles assigned!")

                self.rooms[request.room_name].sync_point.notify_all()
        else:
            async with self.rooms[request.room_name].sync_point:
                await self.rooms[request.room_name].sync_point.wait()

        return mafia_pb2.JoinRoomResponse(flag=True, message="Joined successfully! \n")
    

    async def GetPlayerUpdates(self, request, context):
        cur = self.rooms[request.room_name]
        return mafia_pb2.GetPlayerUpdatesResponse(room_name=request.room_name, username=request.usrename,
                                                  role=cur.assigned_roles[request.username],
                                                  status=cur.statuses[request.username])
    
    async def game_status(self, room):
        print('HERE1')
        if self.rooms[room].room_status == WIN_MAFIA:
            return WIN_MAFIA
        if self.rooms[room].room_status == WIN_INNOCENT:
            return WIN_INNOCENT
        print('HERE2')
        for key, val in self.rooms[room].assigned_roles.items():
            print('HERE3')
            if val == ROLE_MAFIOSI and self.rooms[room].statuses[key] == False:
                print('HERE4')
                return WIN_INNOCENT
        print('HERE5')
        if self.rooms[room].alive_number <= 2 and self.rooms[room].room_status != OVER:
            return WIN_MAFIA
        print('HERE6')
        return ONGOING

 

    async def DayToNight(self, request, context):       
        #adding to queue 
        # start if enough players
        ans = []
        sum_votes = sum(self.rooms[request.room_name].vote_paper.values())
        if self.rooms[request.room_name].waiting >= 3:
            print('entered this')
            async with self.rooms[request.room_name].sync_point:
                self.rooms[request.room_name].killed = None
                max_count = 0
                victim = None
                for value, count in self.rooms[request.room_name].vote_paper.items():
                    if count > max_count:
                        max_count = count
                        victim = value
                    elif count == max_count:
                        victim = None

                self.rooms[request.room_name].killed = victim

                if victim != None:
                    self.rooms[request.room_name].alive_number -= 1
                    self.rooms[request.room_name].statuses[victim] = False

                self.rooms[request.room_name].vote_paper.clear()
                self.rooms[request.room_name].waiting = 0

                status = await self.game_status(request.room_name)
                self.rooms[request.room_name].room_status = status

                self.rooms[request.room_name].sync_point.notify_all()
        else:
            print(f'entered that {request.username}')
            async with self.rooms[request.room_name].sync_point:
                self.rooms[request.room_name].waiting += 1
                await self.rooms[request.room_name].sync_point.wait()

        if self.rooms[request.room_name].killed == None:
            return mafia_pb2.DayToNightResponse(flag=False, victim='', message='No one killed!')

        if self.rooms[request.room_name].room_status != ONGOING:
            return mafia_pb2.DayToNightResponse(flag=True, victim=self.rooms[request.room_name].killed, 
                                                message=self.rooms[request.room_name].room_status)
        return mafia_pb2.DayToNightResponse(flag=False, victim=self.rooms[request.room_name].killed, message='Someone died!')
    

    async def NightToDay(self, request, context):
        sum_votes = sum(self.rooms[request.room_name].vote_paper.values())
        victim = None
        if self.rooms[request.room_name].waiting >= 3:
            self.rooms[request.room_name].killed = None
            print('entered this')
            async with self.rooms[request.room_name].sync_point:
                for key, val in self.rooms[request.room_name].vote_paper.items():
                    if key != '':
                        print('victim chosen')
                        victim = key
                
                self.rooms[request.room_name].alive_number -= 1
                self.rooms[request.room_name].statuses[victim] = False
                self.rooms[request.room_name].killed = victim
                self.rooms[request.room_name].vote_paper.clear()
                self.rooms[request.room_name].waiting = 0

                status = await self.game_status(request.room_name)
                self.rooms[request.room_name].room_status = status

                self.rooms[request.room_name].sync_point.notify_all()
        else:
            print('entered that')
            async with self.rooms[request.room_name].sync_point:
                self.rooms[request.room_name].waiting += 1
                await self.rooms[request.room_name].sync_point.wait()

        print('survived1')
        if self.rooms[request.room_name].room_status != ONGOING:
            return mafia_pb2.NightToDayResponse(flag=True, victim=self.rooms[request.room_name].killed, message=self.rooms[request.room_name].room_status)
        print('survived2')
        return mafia_pb2.NightToDayResponse(flag=False, victim=self.rooms[request.room_name].killed, message=self.rooms[request.room_name].room_status)


    async def GetPlayers(self, request, context):
        cur = self.rooms[request.room_name]
        roles_list = list()
        for player in cur.players:
            if cur.statuses[player] == False:
                roles_list.append(ROLE_DEAD)
            else:
                roles_list.append(cur.assigned_roles[player])
        
        return mafia_pb2.GetPlayersResponse(room_name=request.room_name, names=cur.players,
                                                  roles=roles_list)
    

    def GetGameStatus(self, request, context):
        print(f"State of play in room {request.room_name} was requested")
        cur = self.rooms[request.room_name]

        return mafia_pb2.GetGameStatusResponse()
    

    def VotePaper(self, request, context):

        self.rooms[request.room_name].vote_paper[request.victim] += 1
        return mafia_pb2.VotePaperResponse(status=True)




async def serve(host, port) -> None:
    server = grpc.aio.server()
    mafia_pb2_grpc.add_MafiaServicer_to_server(MafiaServicer(), server)
    listen_addr = "{}:{}".format(host, port)
    server.add_insecure_port(listen_addr)
    print("Running server...")
    await server.start()
    await server.wait_for_termination()


os.environ['HOST'] = host
os.environ['PORT'] = port

if __name__ == '__main__':
    asyncio.run(serve(os.environ['HOST'], os.environ['PORT']))
