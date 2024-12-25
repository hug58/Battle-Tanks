from typing import Union, Dict
import pickle
import struct
import math

from src.commons.collision import Collision
from src.sprites.player import Player

BUFFER_SIZE_INIT_PLAYER = 4
BUFFER_SIZE_EVENT = 1
BUFFER_SIZE_NAME = 32


class Struct:
    """
        Class for packing and unpacking data
    """
    MAX_PLAYERS = 2

    BUFFER_SIZE_PLAYER = 40 * MAX_PLAYERS
    BUFFER_SIZE_NAME = 32
    BUFFER_SIZE_EVENT = 1

    OK_MESSAGE = b'\x01'
    JOIN_MESSAGE = b'\x02'
    USER_NOT_AVAILABLE = b'\x09'
    CLOSE_CONN = b'\x10'

    LEFT_EVENT_PLAYER: bytes = b'\x03'
    RIGHT_EVENT_PLAYER: bytes = b'\x04'
    UP_EVENT_PLAYER: bytes = b'\x05'
    DOWN_EVENT_PLAYER: bytes = b'\x06'
    SHOOT_EVENT_PLAYER: bytes = b'\x06'

    """ LEFT TOWERS """
    LEFT_ANGLE_EVENT_PLAYER: bytes = b'\x07'
    RIGHT_ANGLE_EVENT_PLAYER: bytes = b'\x08'

    UPDATE_PLAYER: int = 1
    NEW_PLAYER: int = 2
    OLD_PLAYER: int = 3

    MOVES = [
            LEFT_EVENT_PLAYER,
             RIGHT_EVENT_PLAYER,
             UP_EVENT_PLAYER, DOWN_EVENT_PLAYER,

             #TOWERS MOVES
             LEFT_ANGLE_EVENT_PLAYER,
             RIGHT_ANGLE_EVENT_PLAYER
             ]

    @staticmethod
    def unpack_single_data(data: bytes) -> tuple:
        """ :param data: bytes"""
        return struct.unpack('B', data)

    @staticmethod
    def pack_single_data(data) -> bytes:
        """ :param data: example: 1"""
        return struct.pack('B', data)

    @staticmethod
    def unpack_player(data: bytes):
        """ :param data: bytes. a player is 6 bytes"""
        return struct.unpack('BBhhhh', data)

    @staticmethod
    def pack_player(data: Union[bytes, None],
                    player_data: dict,
                    status=None) -> bytes:
        """
        pack only the basics (max 6 bytes).

        :param data: moves or fire on bytes.
        :param player_data: Player
        :param status: default is UPDATE_PLAYER

        :return: bytes (STATUS, POSITION, POSX, POSY, CANNONX, CANNONY, ANGLE)
        """

        angle = player_data["angle"]
        angle_cannon = player_data["angle_cannon"]
        radians = math.radians(angle)

        if data in Struct.MOVES:
            if data == Struct.RIGHT_EVENT_PLAYER:
                # player_data["x"] = player_data.get("x") + Player.SPEED
                angle += Player.ANGLE * Player.ANGLE_RIGHT
                angle_cannon += Player.ANGLE * Player.ANGLE_RIGHT

            elif data == Struct.LEFT_EVENT_PLAYER:
                # player_data["x"] = player_data.get("x") - Player.SPEED
                angle -= Player.ANGLE * Player.ANGLE_RIGHT
                angle_cannon += Player.ANGLE * Player.ANGLE_LEFT

            if data == Struct.UP_EVENT_PLAYER or data == Struct.DOWN_EVENT_PLAYER:
                vlx = Player.SPEED * - math.sin(radians)
                vly = Player.SPEED * - math.cos(radians)

                if data == Struct.UP_EVENT_PLAYER:
                    player_data["y"] += vly
                    player_data["x"] += vlx


                elif data == Struct.DOWN_EVENT_PLAYER:
                    player_data["y"] -= vly
                    player_data["x"] -= vlx

            if data == Struct.LEFT_ANGLE_EVENT_PLAYER:
                angle_cannon += Player.ANGLE * Player.ANGLE_LEFT
            elif data == Struct.RIGHT_ANGLE_EVENT_PLAYER:
                angle_cannon += Player.ANGLE * Player.ANGLE_RIGHT

        current = player_data["position"]
        pos_x = player_data["x"]
        pos_y = player_data["y"]

        if math.sqrt(angle ** 2) >= 360:
            angle = 0

        if math.sqrt(angle_cannon ** 2) >= 360:
            angle_cannon = 0

        player_data["angle"] = angle
        player_data["angle_cannon"] = angle_cannon

        Collision.collide_with_objects(player_data)


        return struct.pack('BBhhhh', status if status is not None else Struct.UPDATE_PLAYER,
                           current, int(pos_x), int(pos_y), angle, angle_cannon)


    @staticmethod
    def unpack(data: bytes):
        """ decode data """
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            return data.decode('utf-8')

    @staticmethod
    def unpack_players(data: bytes):
        """ Decode data in chunks of 14 bytes if data length is greater than 14. """
        players = []
        chunk_size = 10

        # Check if data length is greater than 14
        if len(data) > chunk_size:
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                player = Struct.unpack_player(chunk)  # Assuming unpack_player is defined in Struct
                players.append(player)
        else:
            # Handle case where data is less than or equal to 14 bytes
            if len(data) > 0:
                player = Struct.unpack_player(data)  # Unpack the entire data if it's less than or equal to 14 bytes
                players.append(player)

        return players

    @staticmethod
    def pack_players(data: Dict[int, dict], status = None):
        data_encoded = b''
        for d, item in data.items():
            data_encoded += Struct.pack_player(None, item, status)

        return data_encoded

    @staticmethod
    def pack(data: Union[str, dict]):
        """:param data: str or object.  encode data. deprecate. """
        try:
            return pickle.dumps(data)
        except pickle.PicklingError as e:
            return data.encode('utf-8')
