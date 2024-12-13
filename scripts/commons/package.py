
from typing import Union
import pickle
import struct
import math
from scripts.sprites.player import Player

BUFFER_SIZE_INIT_PLAYER = 4
BUFFER_SIZE_EVENT = 1
BUFFER_SIZE_NAME = 32


class Struct:
    """
        Class for packing and unpacking data
    """
    BUFFER_SIZE_PLAYER = 16
    BUFFER_SIZE_NAME = 32
    BUFFER_SIZE_EVENT = 1

    OK_MESSAGE = b'\x01'
    JOIN_MESSAGE = b'\x02'
    USER_NOT_AVAILABLE = b'\x09'

    LEFT_EVENT_PLAYER:bytes  = b'\x03'
    RIGHT_EVENT_PLAYER:bytes = b'\x04'
    UP_EVENT_PLAYER:bytes    = b'\x05'
    DOWN_EVENT_PLAYER:bytes  = b'\x06'
    SHOOT_EVENT_PLAYER:bytes = b'\x06'

    """ LEFT TOWERS """
    LEFT_ANGLE_EVENT_PLAYER:bytes  = b'\x07'
    RIGHT_ANGLE_EVENT_PLAYER:bytes = b'\x08'


    UPDATE_PLAYER:int = 1
    NEW_PLAYER:int = 2
    OLD_PLAYER:int = 3

    MOVES = [LEFT_EVENT_PLAYER, RIGHT_EVENT_PLAYER,
             UP_EVENT_PLAYER,DOWN_EVENT_PLAYER,

             #TOWERS MOVES
             LEFT_ANGLE_EVENT_PLAYER,
             RIGHT_ANGLE_EVENT_PLAYER
             ]


    @staticmethod
    def unpack_single_data(data:bytes) -> tuple:
        """ :param data: bytes"""
        return struct.unpack('B', data)


    @staticmethod
    def pack_single_data(data) -> bytes:
        """ :param data: example: 1"""
        return struct.pack('B', data)


    @staticmethod
    def unpack_player(data:bytes):
        """ :param data: bytes. a player is 6 bytes"""
        return struct.unpack('BBhhhhhh', data)


    @staticmethod
    def pack_player(data: Union[bytes,None], player_data:dict, status = None) -> bytes:
        """
        pack only the basics (max 6 bytes).

        :param data: moves or fire on bytes.
        :param player_data: Player
        :param status: default is UPDATE_PLAYER

        :return: bytes (STATUS, POSITION, POSX, POSY, CANNONX, CANNONY, ANGLE)
        """

        angle = player_data["angle"]
        angle_cannon = player_data["angle_cannon"]

        if data in Struct.MOVES:
            if data == Struct.RIGHT_EVENT_PLAYER:
                player_data["x"] = player_data.get("x") + Player.SPEED
                angle += Player.ANGLE * Player.ANGLE_RIGHT

            elif data == Struct.LEFT_EVENT_PLAYER:
                player_data["x"] = player_data.get("x") - Player.SPEED
                angle += Player.ANGLE * Player.ANGLE_RIGHT

            elif data == Struct.UP_EVENT_PLAYER:
                player_data["y"] = player_data.get("y") - Player.SPEED
            elif data == Struct.DOWN_EVENT_PLAYER:
                player_data["y"] = player_data.get("y") + Player.SPEED

            if data == Struct.LEFT_ANGLE_EVENT_PLAYER:
                angle_cannon += Player.ANGLE * Player.ANGLE_LEFT
            elif data == Struct.RIGHT_ANGLE_EVENT_PLAYER:
                angle_cannon += Player.ANGLE * Player.ANGLE_RIGHT


        current = player_data["position"]
        pos_x = player_data["x"]
        pos_y = player_data["y"]
        cannon_x = player_data["cannon_x"]
        cannon_y = player_data["cannon_y"]

        if math.sqrt(angle ** 2) >= 360:
            angle = 0

        if math.sqrt(angle_cannon ** 2) >= 360:
            angle_cannon = 0

        player_data["angle"] = angle
        player_data["angle_cannon"] = angle_cannon

        return struct.pack('BBhhhhhh', status if status is not None else Struct.UPDATE_PLAYER,
                           current, pos_x, pos_y, cannon_x, cannon_y, angle, angle_cannon)


    @staticmethod
    def unpack(data: bytes):
        """ decode data """
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            return data.decode('utf-8')


    @staticmethod
    def pack(data: Union[str,dict]):
        """:param data: str or object.  encode data. deprecate. """
        try:
            return pickle.dumps(data)
        except pickle.PicklingError as e:
            return data.encode('utf-8')



