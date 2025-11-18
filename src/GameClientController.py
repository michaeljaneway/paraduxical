import asyncio
import threading
from dataclasses import asdict
from typing import Callable

import requests
import websockets

from backend.Board import Cell
from shared.Coordinate import Coordinate
from shared.enums import BoardLayout, Direction, TokenType
from shared.enums.MoveType import MoveType
from shared.TokenLine import TokenLine


class GameClientController:
    def __init__(self, message_callback: Callable[[str], None]) -> None:
        self._message_callback = message_callback
        self._port = "8000"
        self._http_api = f"http://127.0.0.1:{self._port}"
        self._ws_api = f"ws://127.0.0.1:{self._port}/ws"
        self.start_websocket()

    """Game Initialization & Destruction"""

    def create_game(self, board_layout: BoardLayout) -> None:
        body = {"board_layout": board_layout.value}
        r = requests.post(f"{self._http_api}/game", json=body)
        r.raise_for_status()

    def clear_game(self) -> None:
        r = requests.delete(f"{self._http_api}/game")
        r.raise_for_status()

    """Movement Direction"""

    def get_move_type(self) -> MoveType:
        r = requests.get(f"{self._http_api}/move_type")
        r.raise_for_status()
        return r.json()

    def set_move_type(self, move_type: MoveType):
        body = {"move_type": move_type}
        r = requests.post(f"{self._http_api}/move_type", json=body)
        r.raise_for_status()

    """Coordinate Selection"""

    def deselect_coords(self):
        r = requests.delete(f"{self._http_api}/coordinates")
        r.raise_for_status()

    def get_selected_coords(self) -> list[Coordinate]:
        r = requests.get(f"{self._http_api}/coordinates")
        r.raise_for_status()
        coords_json: list[dict] = r.json()
        return [Coordinate(**coord) for coord in coords_json]

    def get_selectable_coords(self) -> list[Coordinate]:
        r = requests.get(f"{self._http_api}/selectable_coordinates")
        r.raise_for_status()
        coords_json: list[dict] = r.json()
        return [Coordinate(**coord) for coord in coords_json]

    def select_coord(self, c: Coordinate):
        r = requests.post(f"{self._http_api}/select_coordinate", json=asdict(c))
        r.raise_for_status()

    """Direction Selection"""

    def get_shift_direction(self) -> Direction:
        r = requests.get(f"{self._http_api}/shift_direction")
        r.raise_for_status()
        return r.json()

    def set_shift_direction(self, direction: Direction):
        body = {"direction": direction}
        r = requests.post(f"{self._http_api}/save_game", json=body)
        r.raise_for_status()

    def get_valid_shift_directions(self) -> list[Direction]:
        r = requests.get(f"{self._http_api}/valid_shift_directions")
        r.raise_for_status()
        return r.json()

    """Movement Execution"""

    def play_move(self) -> None:
        r = requests.post(f"{self._http_api}/play_move")
        r.raise_for_status()

    def is_move_playable(self) -> bool:
        r = requests.post(f"{self._http_api}/is_move_playable")
        r.raise_for_status()
        return r.json()

    """Game State"""

    def is_game_active(self) -> bool:
        r = requests.get(f"{self._http_api}/is_game_active")
        r.raise_for_status()
        return r.json()

    def get_active_player(self) -> TokenType:
        r = requests.get(f"{self._http_api}/active_player")
        r.raise_for_status()
        return TokenType(r.json())

    def get_board_array(self) -> list[list[Cell]]:
        r = requests.get(f"{self._http_api}/board_array")
        r.raise_for_status()

        board_dict_list: list[list[tuple[tuple[int, int, int], int]]] = r.json()
        board_list = [[Cell(Coordinate(*tile[0]), TokenType(tile[1])) for tile in row] for row in board_dict_list]

        return board_list

    def get_board_dict(self) -> dict[Coordinate, TokenType]:
        r = requests.get(f"{self._http_api}/board_dict")
        r.raise_for_status()

        dict_list: list[tuple[tuple[int, int, int], int]] = r.json()
        board_dict = {Coordinate(*item[0]): TokenType(item[1]) for item in dict_list}

        return board_dict

    def get_winning_lines(self) -> list[TokenLine]:
        r = requests.get(f"{self._http_api}/winning_lines")
        r.raise_for_status()
        return r.json()

    """Game Saving & Loading"""

    def save_game(self, save_name: str) -> None:
        body = {"save_name": save_name}
        r = requests.post(f"{self._http_api}/save_game", json=body)
        r.raise_for_status()

    def get_save_games(self) -> list[str]:
        r = requests.get(f"{self._http_api}/save_games")
        r.raise_for_status()
        return r.json()

    def load_game(self, save_name: str) -> None:
        body = {"save_name": save_name}
        r = requests.post(f"{self._http_api}/load_game", json=body)
        r.raise_for_status()

    """WebSocket"""

    def start_websocket(self):
        t = threading.Thread(target=self.begin_ws_connection, daemon=True)
        t.start()

    def begin_ws_connection(self):
        asyncio.run(self.connect_websocket())

    async def connect_websocket(self):
        async with websockets.connect(self._ws_api) as ws:
            while True:
                try:
                    event = await ws.recv()
                    self._message_callback(f"Received: {event}")
                except websockets.exceptions.ConnectionClosedOK:
                    self._message_callback(f"Connection closed normally")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    self._message_callback(f"Connection closed with an error: {e}")
                    break
