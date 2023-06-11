# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mafia.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmafia.proto\x12\x05mafia\")\n\x06Player\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x61live\x18\x02 \x01(\x08\"8\n\x11\x43reateRoomRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\troom_name\x18\x02 \x01(\t\"3\n\x12\x43reateRoomResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"6\n\x0fJoinRoomRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\troom_name\x18\x02 \x01(\t\"1\n\x10JoinRoomResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"4\n\rActionRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"/\n\x0e\x41\x63tionResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"8\n\x11\x43hatStreamRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"E\n\x12\x43hatStreamResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"J\n\x12SendMessageRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x11\n\troom_name\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"h\n\x13SendMessageResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x14\n\x07warning\x18\x04 \x01(\tH\x00\x88\x01\x01\x42\n\n\x08_warning\"G\n\x10VotePaperRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x0e\n\x06victim\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\"1\n\x11VotePaperResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\x12\x0c\n\x04info\x18\x02 \x01(\t\"H\n\x11KillPlayerRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x0e\n\x06victim\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\"3\n\x12KillPlayerResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\";\n\x14GetGameStatusRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"K\n\x15GetGameStatusResponse\x12\x0f\n\x07players\x18\x01 \x03(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0f\n\x07winners\x18\x03 \x03(\t\">\n\x17GetPlayerUpdatesRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"]\n\x18GetPlayerUpdatesResponse\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0c\n\x04role\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\"&\n\x11GetPlayersRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\"E\n\x12GetPlayersResponse\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\r\n\x05names\x18\x02 \x03(\t\x12\r\n\x05roles\x18\x03 \x03(\t\"8\n\x11\x44\x61yToNightRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\"T\n\x12\x44\x61yToNightResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x0e\n\x06victim\x18\x02 \x01(\t\x12\x14\n\x07message\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\n\n\x08_message\"H\n\x11NightToDayRequest\x12\x11\n\troom_name\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0e\n\x06victim\x18\x03 \x01(\t\"T\n\x12NightToDayResponse\x12\x0c\n\x04\x66lag\x18\x01 \x01(\x08\x12\x0e\n\x06victim\x18\x02 \x01(\t\x12\x14\n\x07message\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\n\n\x08_message\"$\n\x10\x43heckUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"$\n\x11\x43heckUserResponse\x12\x0f\n\x07isMafia\x18\x01 \x01(\x08\x32\xf8\x06\n\x05Mafia\x12\x37\n\x06\x41\x63tion\x12\x14.mafia.ActionRequest\x1a\x15.mafia.ActionResponse0\x01\x12\x43\n\nChatStream\x12\x18.mafia.ChatStreamRequest\x1a\x19.mafia.ChatStreamResponse0\x01\x12\x44\n\x0bSendMessage\x12\x19.mafia.SendMessageRequest\x1a\x1a.mafia.SendMessageResponse\x12;\n\x08JoinRoom\x12\x16.mafia.JoinRoomRequest\x1a\x17.mafia.JoinRoomResponse\x12\x41\n\nCreateRoom\x12\x18.mafia.CreateRoomRequest\x1a\x19.mafia.CreateRoomResponse\x12J\n\rGetGameStatus\x12\x1b.mafia.GetGameStatusRequest\x1a\x1c.mafia.GetGameStatusResponse\x12\x41\n\nGetPlayers\x12\x18.mafia.GetPlayersRequest\x1a\x19.mafia.GetPlayersResponse\x12>\n\tCheckUser\x12\x17.mafia.CheckUserRequest\x1a\x18.mafia.CheckUserResponse\x12\x41\n\nKillPlayer\x12\x18.mafia.KillPlayerRequest\x1a\x19.mafia.KillPlayerResponse\x12>\n\tVotePaper\x12\x17.mafia.VotePaperRequest\x1a\x18.mafia.VotePaperResponse\x12S\n\x10GetPlayerUpdates\x12\x1e.mafia.GetPlayerUpdatesRequest\x1a\x1f.mafia.GetPlayerUpdatesResponse\x12\x41\n\nDayToNight\x12\x18.mafia.DayToNightRequest\x1a\x19.mafia.DayToNightResponse\x12\x41\n\nNightToDay\x12\x18.mafia.NightToDayRequest\x1a\x19.mafia.NightToDayResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mafia_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PLAYER._serialized_start=22
  _PLAYER._serialized_end=63
  _CREATEROOMREQUEST._serialized_start=65
  _CREATEROOMREQUEST._serialized_end=121
  _CREATEROOMRESPONSE._serialized_start=123
  _CREATEROOMRESPONSE._serialized_end=174
  _JOINROOMREQUEST._serialized_start=176
  _JOINROOMREQUEST._serialized_end=230
  _JOINROOMRESPONSE._serialized_start=232
  _JOINROOMRESPONSE._serialized_end=281
  _ACTIONREQUEST._serialized_start=283
  _ACTIONREQUEST._serialized_end=335
  _ACTIONRESPONSE._serialized_start=337
  _ACTIONRESPONSE._serialized_end=384
  _CHATSTREAMREQUEST._serialized_start=386
  _CHATSTREAMREQUEST._serialized_end=442
  _CHATSTREAMRESPONSE._serialized_start=444
  _CHATSTREAMRESPONSE._serialized_end=513
  _SENDMESSAGEREQUEST._serialized_start=515
  _SENDMESSAGEREQUEST._serialized_end=589
  _SENDMESSAGERESPONSE._serialized_start=591
  _SENDMESSAGERESPONSE._serialized_end=695
  _VOTEPAPERREQUEST._serialized_start=697
  _VOTEPAPERREQUEST._serialized_end=768
  _VOTEPAPERRESPONSE._serialized_start=770
  _VOTEPAPERRESPONSE._serialized_end=819
  _KILLPLAYERREQUEST._serialized_start=821
  _KILLPLAYERREQUEST._serialized_end=893
  _KILLPLAYERRESPONSE._serialized_start=895
  _KILLPLAYERRESPONSE._serialized_end=946
  _GETGAMESTATUSREQUEST._serialized_start=948
  _GETGAMESTATUSREQUEST._serialized_end=1007
  _GETGAMESTATUSRESPONSE._serialized_start=1009
  _GETGAMESTATUSRESPONSE._serialized_end=1084
  _GETPLAYERUPDATESREQUEST._serialized_start=1086
  _GETPLAYERUPDATESREQUEST._serialized_end=1148
  _GETPLAYERUPDATESRESPONSE._serialized_start=1150
  _GETPLAYERUPDATESRESPONSE._serialized_end=1243
  _GETPLAYERSREQUEST._serialized_start=1245
  _GETPLAYERSREQUEST._serialized_end=1283
  _GETPLAYERSRESPONSE._serialized_start=1285
  _GETPLAYERSRESPONSE._serialized_end=1354
  _DAYTONIGHTREQUEST._serialized_start=1356
  _DAYTONIGHTREQUEST._serialized_end=1412
  _DAYTONIGHTRESPONSE._serialized_start=1414
  _DAYTONIGHTRESPONSE._serialized_end=1498
  _NIGHTTODAYREQUEST._serialized_start=1500
  _NIGHTTODAYREQUEST._serialized_end=1572
  _NIGHTTODAYRESPONSE._serialized_start=1574
  _NIGHTTODAYRESPONSE._serialized_end=1658
  _CHECKUSERREQUEST._serialized_start=1660
  _CHECKUSERREQUEST._serialized_end=1696
  _CHECKUSERRESPONSE._serialized_start=1698
  _CHECKUSERRESPONSE._serialized_end=1734
  _MAFIA._serialized_start=1737
  _MAFIA._serialized_end=2625
# @@protoc_insertion_point(module_scope)
