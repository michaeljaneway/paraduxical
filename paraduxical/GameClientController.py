import asyncio
import threading
from dataclasses import asdict
from typing import Any, Callable

import requests
import websockets

from backend.Board import Cell
from shared.Coordinate import Coordinate
from shared.enums import BoardLayout, Direction, GameEvent, MoveType, TokenType
from shared.TokenLine import TokenLine


class GameClientController:
    def __init__(self, port: int) -> None:
        # Connection information
        self._port = str(port)
        self._http_api = f"http://127.0.0.1:{self._port}"
        self._ws_api = f"ws://127.0.0.1:{self._port}/ws"

        # Event handling
        self._event_generator: Callable[[GameEvent], None] | None = None
        self._error_callback: Callable[[str], None] | None = None

        # When set to false, will end the websocket thread
        self.should_websocket_be_active: bool = True

        # The pseudo-viewmodel
        self.model = GameModelProxy(self)
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
        return MoveType(r.json())

    def set_move_type(self, move_type: MoveType):
        body = {"move_type": move_type}
        r = requests.post(f"{self._http_api}/move_type", json=body)
        r.raise_for_status()

    """Coordinate Selection"""

    def deselect_coord(self, c: Coordinate):
        r = requests.post(f"{self._http_api}/deselect_coordinate", json=asdict(c))
        r.raise_for_status()

    def select_coord(self, c: Coordinate):
        r = requests.post(f"{self._http_api}/select_coordinate", json=asdict(c))
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

    """Direction Selection"""

    def get_shift_direction(self) -> Direction:
        r = requests.get(f"{self._http_api}/shift_direction")
        r.raise_for_status()
        return Direction(r.json())

    def set_shift_direction(self, direction: Direction):
        body = {"direction": direction}
        r = requests.post(f"{self._http_api}/shift_direction", json=body)
        r.raise_for_status()

    def get_valid_shift_directions(self) -> list[Direction]:
        r = requests.get(f"{self._http_api}/valid_shift_directions")
        r.raise_for_status()

        dir_list = r.json()
        return [Direction(d) for d in dir_list]

    """Movement Execution"""

    def play_move(self) -> None:
        r = requests.post(f"{self._http_api}/play_move")
        r.raise_for_status()

    def is_move_playable(self) -> bool:
        r = requests.get(f"{self._http_api}/is_move_playable")
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

        lines_json = r.json()
        lines: list[TokenLine] = []

        for line in lines_json:
            lines.append(TokenLine(TokenType(line["token_type"]), [Coordinate(coord["q"], coord["r"], coord["s"]) for coord in line["coords"]]))

        return lines

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

    """WebSocket Initialization"""

    def start_websocket(self):
        self.ws_thread = threading.Thread(target=lambda: asyncio.run(self.run_websocket()), daemon=True)
        self.ws_thread.start()

    async def run_websocket(self):
        async with websockets.connect(self._ws_api) as ws:
            while self.should_websocket_be_active:
                try:
                    event = await ws.recv()
                    if not event in GameEvent._value2member_map_:
                        continue
                    self._generate_event(GameEvent(event))
                except websockets.exceptions.ConnectionClosedOK:
                    if self._error_callback:
                        self._error_callback(f"Connection closed normally")
                    break
                except websockets.exceptions.ConnectionClosedError as e:
                    if self._error_callback:
                        self._error_callback(f"Connection closed with an error: {e}")
                    break

    """Websocket Event Generation"""

    def set_event_handler(self, event_generator: Callable[[GameEvent], None]):
        self._event_generator = event_generator

    def set_error_callback(self, error_callback: Callable[[str], None]):
        self._error_callback = error_callback

    def _generate_event(self, event: GameEvent):
        if not self._event_generator:
            return

        self.model.refresh_all_data()
        self._event_generator(event)


class GameModelProxy:
    """A pseudo-viewmodel to prevent excessive API calls"""

    def __init__(self, controller: GameClientController) -> None:
        self._controller = controller
        self.refresh_all_data()

    def refresh_all_data(self):
        # Game State
        self.is_game_active: bool = self._controller.is_game_active()
        self.game_saves: list[str] = self._controller.get_save_games()

        if not self.is_game_active:
            return

        self.active_player: TokenType = self._controller.get_active_player()

        # Board
        self.board_2d: list[list[Cell]] = self._controller.get_board_array()
        self.board_dict: dict[Coordinate, TokenType] = self._controller.get_board_dict()
        self.winning_lines: list[TokenLine] = self._controller.get_winning_lines()

        # Moving
        self.is_move_playable: bool = self._controller.is_move_playable()
        self.move_type: MoveType = self._controller.get_move_type()
        self.direction: Direction = self._controller.get_shift_direction()
        self.valid_shift_directions: list[Direction] = self._controller.get_valid_shift_directions()
        self.selected_coords: list[Coordinate] = self._controller.get_selected_coords()
        self.selectable_coords: list[Coordinate] = self._controller.get_selectable_coords()
