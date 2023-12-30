from src.actor import Actor
from src.constants import Color, Piece, colors, MapParsed, map_points, MapRaw, nb_line_piece
from src.controller import Controller

class Model:
    __map: MapParsed = []
    __controller: Controller = None

    def set_map(self, new_map: MapRaw) -> MapParsed:
        self.__map = [ [ int(c) for c in line ] for line in new_map ]
        return self.__map

    def get_map(self) -> MapParsed:
        return self.__map
    
    def is_valid_position(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        if y >= len(self.__map) or x >= len(self.__map[0]):
            return False
        return self.__map[y][x] == map_points['destination_point']
    
    def is_valid_move(self, x0: int, y0: int, x1: int, y1: int) -> bool:
        # make difference to get direction
        dx = x1 - x0
        dy = y1 - y0
        if dx == 0 and dy == 0:
            # same position
            return False
        elif dx != 0 and dy != 0:
            # diagonal move
            return False
        
        # check points is in map
        if x0 < 0 or y0 < 0 or x1 < 0 or y1 < 0:
            return False
        if y0 >= len(self.__map[0]) or y1 >= len(self.__map):
            return False
        
        if self.__map[y0][x0] == map_points['empty'] or self.__map[y1][x1] == map_points['empty']:
            return False
        
        # check if there is a way between the two points
        # check horizontal move
        indestination = False
        for i in range(0, dx, 1 if dx > 0 else -1):
            if self.__map[y0][x0 + i] == map_points['destination_point'] and not indestination:
                indestination = True
            elif self.__map[y0][x0 + i] != map_points['way']:
                return False
        # check vertical move
        indestination = False
        for i in range(0, dy, 1 if dy > 0 else -1):
            if self.__map[y0 + i][x0] == map_points['destination_point'] and not indestination:
                indestination = True
            elif self.__map[y0 + i][x0] != map_points['way']:
                return False
            
        return True
    
    def set_controller(self, controller: Controller):
        self.__controller = controller

    __players: list[Actor] = []
    def get_players(self):
        return self.__players
    
    def add_player(self, player: Actor):
        player.set_instance(self)
        self.__players.append(player)
        self.__controller.update()

    def remove_player(self, player: Actor):
        self.__players.remove(player)
        self.__controller.update()
        

    def choise_color(self):
        used = [ player.get_color() for player in self.__players ]
        colors_unsing = {}
        for color in used:
            colors_unsing[color] = colors_unsing.get(color, 0) + 1
        max_color_reused = 0
        for color in colors_unsing:
            if colors_unsing[color] > max_color_reused:
                max_color_reused = colors_unsing[color]
        unused_colors: list[Color] = colors * (max_color_reused + 1)
        for color in used:
            unused_colors.remove(color)
        return unused_colors[0]
    
    def start_game(self):
        for player in self.__players:
            player.reset()
        self.__controller.update()
        self.__turn_player(self.__players[0])
        
    def get_players_in_game(self) -> list[Actor]:
        return list(filter(lambda x: x.get_max_pieces() >= nb_line_piece, self.__players))
    
    def get_winner(self) -> Actor | None:
        players = self.get_players_in_game()
        if len(players) == 1:
            self.__controller.add_log(self.__controller.lang_get('player_win', values=(players[0].get_name(),)))
            return players[0]
        return None
    
    def player_add_piece(self, player: Actor, piece: Piece) -> list[Piece]:
        if player not in self.__players:
            return None
        self.__controller.add_log(self.__controller.lang_get('player_add_piece', values=(player.get_name(), piece)))
        player.add_piece(piece)
        self.__controller.update()
        return piece
    
    def player_move_piece(self, player: Actor, piece: Piece, x: int, y: int) -> Piece:
        player.remove_piece(piece)
        self.__controller.add_log(self.__controller.lang_get('player_move_piece', values=(player.get_name(), piece, (x, y))))
        player.add_piece((x, y))
        self.__controller.update()
        return (x, y)
    
    def get_all_pieces(self) -> list[Piece]:
        pieces: list[Piece] = []
        for player in self.__players:
            pieces += player.get_pieces()
        return pieces
    
    def player_remove_piece(self, player: Actor, piece: Piece) -> list[Piece]:
        if player not in self.__players:
            return None
        player.remove_piece(piece)
        self.__controller.update()
        return piece
    
    def __turn_player(self, player: Actor):
        if player not in self.__players:
            return None
        self.__controller.add_log(self.__controller.lang_get('player_turn', values=(player.get_name(),)))
        
        def select_other_piece(x: int, y: int):
            other_player = None
            for i in self.__players:
                if (x, y) in i.get_pieces():
                    other_player = i
                    break
            if other_player is None or other_player == player:
                return False
            self.player_remove_piece(other_player, (x, y))
            other_player.set_max_pieces(other_player.get_max_pieces() - 1)
            if other_player.get_max_pieces() == 0:
                self.__controller.add_log(self.__controller.lang_get('player_eliminated', values=(other_player.get_name(), player.get_name())))
            else:
                self.__controller.add_log(self.__controller.lang_get('player_loss_piece', values=(other_player.get_name(), (x, y), other_player.get_max_pieces())))
            post_end_turn()
            return True
            
        def end_turn(piece: Piece):
            if self.player_has_line(player, piece):
                self.__controller.event_player_remove(player, lambda x, y: select_other_piece(x, y))
                return True
            post_end_turn()
            return True
            
        def post_end_turn():
            self.__players.remove(player)
            self.__players.append(player)
            if self.get_winner() is None:
                self.__turn_player(self.__players[0])
            else:
                self.__controller.is_winned(self.get_winner())
            self.__controller.update()
            return True
        
        def move_piece(player: Actor, piece: Piece, x: int, y: int):
            if not self.is_valid_move(piece[0], piece[1], x, y):
                return False
            self.player_move_piece(player, piece, x, y)
            end_turn((x, y))
            return True
        
        def select_piece(x: int, y: int):
            if not self.is_valid_position(x, y):
                return False
            if player.owner_piece(x, y):
                self.__controller.event_player_move(player, (x, y), lambda x1, y1: move_piece(player, (x, y), x1, y1))
                return True
            if (x, y) in self.get_all_pieces():
                return False
            if len(player.get_pieces()) >= player.get_max_pieces():
                return False
            self.player_add_piece(player, (x, y))
            end_turn((x, y))
            
            return True
        
        self.__controller.event_player_turn(player, lambda x, y: select_piece(x, y))
    
    def is_winned(self, player: Actor):
        self.__controller.add_log(self.__controller.lang_get('player_win', values=(player.get_name(),)))
        
    def player_has_line(self, player: Actor, inital_piece: Piece) -> bool:
        print('player_has_line', player, inital_piece)
        hor = list(filter(lambda x: x[1] == inital_piece[1], player.get_pieces()))
        hor.sort(key=lambda x: x[0])
        
        max_horizontal = 0
        horizontal = 0
        
        for i in range(len(hor) - 1):
            if self.is_valid_move(hor[i][0], hor[i][1], hor[i+1][0], hor[i+1][1]):
                horizontal += 1
            else:
                max_horizontal = max(max_horizontal, horizontal)
                horizontal = 0
                    
        if horizontal > max_horizontal:
            max_horizontal = horizontal
            
        if max_horizontal + 1 >= nb_line_piece:
            return True
        
        ver = list(filter(lambda x: x[0] == inital_piece[0], player.get_pieces()))
        ver.sort(key=lambda x: x[1])
        print('ver', ver)
        
        max_vertical = 0
        vertical = 0
        
        for i in range(len(ver) - 1):
            if self.is_valid_move(ver[i][0], ver[i][1], ver[i+1][0], ver[i+1][1]):
                vertical += 1
            else:
                max_vertical = max(max_vertical, vertical)
                vertical = 0
                    
        if vertical > max_vertical:
            max_vertical = vertical
        
        if max_vertical + 1 >= nb_line_piece:
            return True
        
        print('max_horizontal', max_horizontal)
        print('max_vertical', max_vertical)
        
        return False
        
        
        
        
    
        
            
        
        
