
from src.constants import Piece
from src.lang import Lang
from src.actor import Actor


class Controller:
    def __init__(self, model: 'Model', view: 'View'):
        self.__model: 'Model' = model
        self.__view: 'View' = view
        self.__lang: 'Lang' = Lang()

        self.__view.set_controller(self)
        self.__model.set_controller(self)

    def run(self):
        self.__view.add_log(self.lang_get('welcome'))
        self.__view.run()

    def get_players(self):
        return self.__model.get_players()
    
    def add_player(self, player: Actor):
        self.__model.add_player(player)
        self.__view.add_log(self.lang_get('player_added', values=(player.get_name(),)))
        self.__view.update()
    
    def lang_get(self, key: str, values: list[str] | None = [], lang: str | None = None) -> str:
        return self.__lang.get(key, values, lang)
    
    def remove_player(self, player: Actor):
        self.__model.remove_player(player)
        self.__view.add_log(self.lang_get('player_removed', values=(player.get_name(),)))
        self.__view.update()
        
    def is_valid_move(self, x0: int, y0: int, x1: int, y1: int):
        return self.__model.is_valid_move(x0, y0, x1, y1)
    
    def is_valid_position(self, x: int, y: int):
        return self.__model.is_valid_position(x, y)
        
    def get_map(self):
        return self.__model.get_map()
    
    def update(self):
        self.__view.update()
        
    def add_log(self, message: str):
        self.__view.add_log(message)
        
    def event_player_turn(self, player: Actor, callback: callable):
        self.__view.event_player_turn(player, callback)
        
    def event_player_move(self, player: Actor, piece: Piece, callback: callable):
        self.__view.event_player_move(player, piece, callback)
        
    def event_player_remove(self, player: Actor, callback: callable):
        self.__view.event_player_remove(player, callback)
        
    def start_game(self):
        self.__model.start_game()
        
    def next_turn(self):
        self.__model.next_turn()
        self.__view.update()