
from typing import Union
import pickle
import struct
from scripts.sprites.player import Player

BUFFER_SIZE_INIT_PLAYER = 4
BUFFER_SIZE_PLAYER = 6
BUFFER_SIZE_EVENT = 1

OK_MESSAGE = b'\x01'
JOIN_MESSAGE = b'\x02'


class Struct:
    """
        Class for packing and unpacking data
    """
    LEFT_EVENT_PLAYER:bytes  = b'\x03'
    RIGHT_EVENT_PLAYER:bytes = b'\x04'
    UP_EVENT_PLAYER:bytes    = b'\x05'
    DOWN_EVENT_PLAYER:bytes  = b'\x06'

    UPDATE_PLAYER:int = 1

    MOVES = [LEFT_EVENT_PLAYER, RIGHT_EVENT_PLAYER, UP_EVENT_PLAYER,DOWN_EVENT_PLAYER]

    @staticmethod
    def unpack_player(data:bytes):
        return struct.unpack('BBhh', data)

    @staticmethod
    def pack_player(data: Union[bytes,None], player_data:dict):
        """ pack only the basics (max 6 bytes). """
        if data in Struct.MOVES:
            if data == Struct.RIGHT_EVENT_PLAYER:
                player_data["x"] = player_data.get("x") + Player.SPEED
            elif data == Struct.LEFT_EVENT_PLAYER:
                player_data["x"] = player_data.get("x") - Player.SPEED
            elif data == Struct.UP_EVENT_PLAYER:
                player_data["y"] = player_data.get("y") - Player.SPEED
            elif data == Struct.DOWN_EVENT_PLAYER:
                player_data["y"] = player_data.get("y") + Player.SPEED

        current = player_data["position"]
        pos_x = player_data["x"]
        pos_y = player_data["y"]
        return struct.pack('BBhh', Struct.UPDATE_PLAYER, current, pos_x, pos_y)


    @staticmethod
    def unpack(data: bytes):
        """ decode data """
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            return data.decode('utf-8')


    @staticmethod
    def pack(data: Union[str,dict]):
        """ encode data """
        try:
            return pickle.dumps(data)
        except pickle.PicklingError as e:
            return data.encode('utf-8')



