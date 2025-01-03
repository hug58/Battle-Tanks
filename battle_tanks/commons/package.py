from typing import Union, Dict
import pickle
import struct
import math

from battle_tanks.components.collision import Collision
from battle_tanks.sprites.player import Player

BUFFER_SIZE_INIT_PLAYER = 4
BUFFER_SIZE_EVENT = 1
BUFFER_SIZE_NAME = 32


class Struct:
    """
        Class for packing and unpacking data
    """
    SIZE_PLAYER = 11
    MAX_PLAYERS = 2
    BUFFER_SIZE_PLAYER = SIZE_PLAYER * MAX_PLAYERS
    BUFFER_SIZE_EVENT_RESPONSE = 10
    BUFFER_SPLIT_MAP = BUFFER_SIZE_EVENT_RESPONSE * 8
    BUFFER_SIZE_LVL_MAP = 40
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

    """ FIRE EVENTS"""
    FIRE_EVENT_PLAYER: bytes = b'\x11'

    UPDATE_PLAYER: int = 1
    NEW_PLAYER: int = 2
    OLD_PLAYER: int = 3


    BROKE_BRICK:int = 4
    BRICK:int = 5
    BLOCK:int = 6

    STATUS_PLAYER = [UPDATE_PLAYER,NEW_PLAYER,OLD_PLAYER]

    MOVES = [
            LEFT_EVENT_PLAYER,
            RIGHT_EVENT_PLAYER,
            UP_EVENT_PLAYER,
            DOWN_EVENT_PLAYER,

            #TOWERS MOVES
            LEFT_ANGLE_EVENT_PLAYER,
            RIGHT_ANGLE_EVENT_PLAYER,

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
        return struct.unpack('BBhhhhb', data)


    @staticmethod
    def pack_player(data: Union[bytes, None],
                    player_data: dict,
                    status=None) -> bytes:
        """
        pack only the basics (max 6 bytes).

        :param data: moves or fire on bytes.
        :param player_data: Player
        :param status: default is UPDATE_PLAYER

        :return: bytes (STATUS, POSITION, X, Y, ANGLE, ANGLE_CANNON, DAMAGE_INDICATOR)
        """
        angle = player_data["angle"]
        angle_cannon = player_data["angle_cannon"]
        radians = math.radians(angle)
        damage_indicator = player_data["damage_indicator"]

        if data in Struct.MOVES:
            if data == Struct.RIGHT_EVENT_PLAYER:
                angle += Player.ANGLE * Player.ANGLE_RIGHT
                angle_cannon += Player.ANGLE * Player.ANGLE_RIGHT
            elif data == Struct.LEFT_EVENT_PLAYER:
                angle -= Player.ANGLE * Player.ANGLE_RIGHT
                angle_cannon += Player.ANGLE * Player.ANGLE_LEFT
            elif data == Struct.LEFT_ANGLE_EVENT_PLAYER:
                angle_cannon += Player.ANGLE * Player.ANGLE_LEFT
            elif data == Struct.RIGHT_ANGLE_EVENT_PLAYER:
                angle_cannon += Player.ANGLE * Player.ANGLE_RIGHT

            if (data == Struct.UP_EVENT_PLAYER or
                    data == Struct.DOWN_EVENT_PLAYER):

                vlx = Player.SPEED * - math.sin(radians)
                vly = Player.SPEED * - math.cos(radians)

                if data == Struct.UP_EVENT_PLAYER:
                    player_data["y"] += vly
                    player_data["x"] += vlx
                elif data == Struct.DOWN_EVENT_PLAYER:
                    player_data["y"] -= vly
                    player_data["x"] -= vlx

                Collision.collide_with_objects(player_data)

        current = player_data["position"]
        pos_x = player_data["x"]
        pos_y = player_data["y"]
        angle = angle % 360
        angle_cannon = angle_cannon % 360

        player_data["angle"] = angle
        player_data["angle_cannon"] = angle_cannon

        return struct.pack('BBhhhhb', status if status is not None else Struct.UPDATE_PLAYER,
                           current, int(pos_x), int(pos_y), angle, angle_cannon, damage_indicator)


    @staticmethod
    def unpack_players(data: bytes) -> list:
        """ Decode data in chunks of 14 bytes if data length is greater than 14. """
        players = []
        chunk_size = Struct.BUFFER_SIZE_PLAYER

        # Check if data length is greater than 14
        if len(data) > chunk_size:
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                player = Struct.unpack_player(chunk)
                players.append(player)
        else:
            if len(data) > 0:
                player = Struct.unpack_player(data)
                players.append(player)

        return players


    @staticmethod
    def pack_players(data: Dict[int, dict], status = None) -> bytes:
        data_encoded = b''
        for d, item in data.items():
            data_encoded += Struct.pack_player(None, item, status)

        return data_encoded

    @staticmethod
    def pack_tile(data: dict):
        return struct.pack("bhhhh", data["type"],data["x"],
                           data["y"],data["w"],data["h"])

    @staticmethod
    def pack_event(player_data: dict) -> Union[bytes, None]:
        data_collided = Collision.check_collision_bullet(player_data, 30)
        if len(data_collided.items()) > 0:
            data_collided["type"] = Struct.BROKE_BRICK
            return Struct.pack_tile(data_collided)

        return None


    @staticmethod
    def unpack_event(data: bytes):
        return struct.unpack('bhhhh', data)


    @staticmethod
    def unpack_events(data: bytes) -> list:
        """ Decode data in chunks of 14 bytes if data length is greater than 14. """
        events = []
        chunk_size = Struct.BUFFER_SIZE_EVENT_RESPONSE

        # Check if data length is greater than 14
        if len(data) > chunk_size:
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i + chunk_size]
                _event = Struct.unpack_event(chunk)
                events.append(_event)
        else:
            if len(data) > 0:
                _event = Struct.unpack_event(data)
                events.append(_event)

        return events


    @staticmethod
    def pack(data: Union[str, dict]):
        """:param data: str or object.  encode data. deprecate. """
        try:
            return pickle.dumps(data)
        except pickle.PicklingError as e:
            return data.encode('utf-8')


    @staticmethod
    def unpack(data: bytes):
        """ decode data """
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            return data.decode('utf-8')