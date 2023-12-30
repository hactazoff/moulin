from src.constants import Piece
from src.actor import Actor
from src.controller import Controller
from src.view import View
import tkinter as tk
from tkinter import ttk
import sys

class ViewGUI(View):

    __controller: Controller = None
    __position_suggestion: Piece | None = None
    __store_canvas = {
        "height": 0,
        "width": 0,
        "lines": []
    }

    def set_controller(self, controller: Controller):
        self.__controller = controller

    def __init__(self):
        super().__init__()
        toplevel1 = tk.Tk()
        toplevel1.geometry('1384x748')
        toplevel1.title('Jeu du Moulin')

        frame13 = ttk.Frame(toplevel1)
        frame13.configure(height=200, width=200)
        frame14 = ttk.Frame(frame13)
        frame14.configure(height=200, width=200)
        canvas1 = tk.Canvas(frame14)
        canvas1.pack(expand=True, fill="both", side="top")
        frame14.pack(expand=True, fill="both", padx=25, pady=25, side="left")
        frame15 = ttk.Frame(frame13)
        frame15.configure(height=200, width=200)
        frame16 = ttk.Frame(frame15)
        frame16.configure(height=200, width=200)
        label1 = ttk.Label(frame16)
        label1.configure(text='Jeu du Moulin')
        label1.pack(side="top")
        treeview1 = ttk.Treeview(frame16)
        treeview1.configure(selectmode="none", show="headings")
        treeview1.pack(expand=False, fill="x", padx=0, pady=25, side="top")
        treeview2 = ttk.Treeview(frame16)
        treeview2.configure(selectmode="extended", show="headings")
        treeview2.pack(expand=True, fill="both", side="top")
        frame18 = ttk.Frame(frame16)
        frame18.configure(height=25, width=0)
        frame18.pack(side="top")
        button6 = ttk.Button(frame16)
        button6.configure(text='Loading...')
        button6.pack(side="top")
        frame16.pack(padx=25, pady=25, side="top")
        frame15.pack(side="right")
        frame13.pack(expand=True, fill="both", side="top")

        self.mainwindow = toplevel1
        self.player_list = treeview1
        self.log_list = treeview2
        self.canvas = canvas1
        self.reload = button6
        
        self.__style = ttk.Style()
        self.__style.theme_use('clam')
        if sys.platform == 'win32':
            import sv_ttk
            sv_ttk.use_light_theme()

        print(self.__style.theme_names())

    def run(self):
        self.player_list['columns'] = ('name', 'pieces', 'color')
        self.player_list.heading('name', text='Joueur')
        self.player_list.heading('pieces', text='Pions')
        self.player_list.heading('color', text='Couleur')
        self.log_list['columns'] = ('log')
        self.log_list.heading('log', text='Informations')
        
        self.calculate_canvas()
        self.update_canvas()
        self.mainwindow.bind('<Configure>', lambda e: self.update_canvas())
        self.canvas.bind('<Motion>', lambda e: self.update_sudggestion(e.x, e.y))
        self.canvas.bind('<Leave>', lambda e: self.update_sudggestion(-1, -1))
        self.canvas.bind('<Button-1>', lambda e: self.on_click())
        self.reload.configure(text='Lancer la partie')
        self.reload.configure(command=lambda: self.start_game())
        self.mainwindow.mainloop()
        
    def start_game(self):
        self.reload.configure(text='Nouvelle partie')
        self.add_log(self.__controller.lang_get('start_game'))
        self.player_turn_callback = None
        self.__controller.start_game()
        
    def on_click(self):
        if self.__position_suggestion is not None:
            try:
                ou = self.player_remove_callback
                print('ou remove', ou)
                self.player_remove_callback = None
                out = not ou(self.__position_suggestion[0], self.__position_suggestion[1])
                if out:
                    self.add_log(self.__controller.lang_get('player_invalid_remove'))
                    self.player_remove_callback = ou
                    return
                return
            except Exception as e:
                try:
                    ou = self.player_move_callback
                    print('ou move', ou)
                    self.player_move_callback = None
                    out = not ou(self.__position_suggestion[0], self.__position_suggestion[1])
                    if out:
                        self.add_log(self.__controller.lang_get('player_invalid_move'))
                        self.player_move_callback = ou
                        return
                    return
                except Exception as e:
                    print('error move', e)
                    try:
                        ou = self.player_turn_callback
                        print('ou turn', ou)
                        self.player_turn_callback = None
                        out = not ou(self.__position_suggestion[0], self.__position_suggestion[1])
                        if out:
                            self.add_log(self.__controller.lang_get('player_invalid_turn'))
                            self.player_turn_callback = ou
                            return
                        return
                    except Exception as e:
                        print('error turn', e)
                
        
    def update_sudggestion(self, x: int, y: int):
        if x < 0 or y < 0:
            self.__position_suggestion = None
            self.update_canvas()
            return
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        wp = max(width / (self.__store_canvas['width']), height / (self.__store_canvas['height'])) /2
        x_on_map = int(x / (width - wp) * (self.__store_canvas['width'] + 1) - 1)
        y_on_map = int(y / (height - wp) * (self.__store_canvas['height'] + 1) - 1)
        if self.__controller.is_valid_position(x_on_map, y_on_map) and (self.__position_suggestion is None or self.__position_suggestion != (x_on_map, y_on_map)):
            self.__position_suggestion = (x_on_map, y_on_map)
            self.update_canvas()

    def update(self):
        players: list[Actor] = self.__controller.get_players()
        for i in self.player_list.get_children():
            self.player_list.delete(i)
        for i in range(len(players)):
            self.player_list.insert('', 'end', text=str(i+1), values=(
                players[i].get_name(), 
                str(len(players[i].get_pieces())) + ' / ' + str(players[i].get_max_pieces()),
                players[i].get_color()
            ))
        self.update_canvas()
        
    def calculate_canvas(self):
        current_map = self.__controller.get_map()
        self.__store_canvas['lines'] = []
        width_map = len(current_map[0])
        height_map = len(current_map)
        self.__store_canvas['width'] = width_map
        self.__store_canvas['height'] = height_map
        for y0 in range(height_map):
            for x0 in range(width_map):
                for y1 in range(height_map):
                    for x1 in range(width_map):
                        if self.__controller.is_valid_move(x0, y0, x1, y1):
                            self.__store_canvas['lines'].append((x0, y0, x1, y1))
        

    def update_canvas(self):
        # get dimensions of canvas
        self.mainwindow.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.delete('all')
        for line in self.__store_canvas['lines']:
            x0_on_canvas = (line[0] + 1) * width / (self.__store_canvas['width'] + 1)
            y0_on_canvas = (line[1] + 1) * height / (self.__store_canvas['height'] + 1)
            x1_on_canvas = (line[2] + 1) * width / (self.__store_canvas['width'] + 1)
            y1_on_canvas = (line[3] + 1) * height / (self.__store_canvas['height'] + 1)
            self.canvas.create_line(x0_on_canvas, y0_on_canvas, x1_on_canvas, y1_on_canvas)
        
        if self.__position_suggestion is not None:
            x_on_canvas = (self.__position_suggestion[0] + 1) * width / (self.__store_canvas['width'] + 1)
            y_on_canvas = (self.__position_suggestion[1] + 1) * height / (self.__store_canvas['height'] + 1)
            wp = min(width / (self.__store_canvas['width'] + 1), height / (self.__store_canvas['height'] + 1)) / 2
            self.canvas.create_oval(
                x_on_canvas - wp-2,
                y_on_canvas - wp-2,
                x_on_canvas + wp+2, 
                y_on_canvas + wp+2,
                fill='gray',
            )
            
        players: list[Actor] = self.__controller.get_players()
        for i in range(len(players)):
            for piece in players[i].get_pieces():
                x_on_canvas = (piece[0] + 1) * width / (self.__store_canvas['width'] + 1)
                y_on_canvas = (piece[1] + 1) * height / (self.__store_canvas['height'] + 1)
                wp = min(width / (self.__store_canvas['width'] + 1), height / (self.__store_canvas['height'] + 1)) / 2
                self.canvas.create_oval(
                    x_on_canvas - wp,
                    y_on_canvas - wp,
                    x_on_canvas + wp, 
                    y_on_canvas + wp,
                    fill=players[i].get_color(),
                )
                
    def add_log(self, message: str):
        self.log_list.insert('', 'end', text=str(len(self.log_list.get_children()) + 1), values=(message,))
        self.log_list.yview_moveto(1)
        
    player_turn_callback: callable
    def event_player_turn(self, player: Actor, callback: callable):
        print('event_player_turn', callback)
        self.add_log(self.__controller.lang_get('player_turn_explan', values=(player.get_name(),)))
        self.player_turn_callback = callback
        
    player_move_callback: callable
    def event_player_move(self, player: Actor, piece: Piece, callback: callable):
        print('event_player_move', callback)
        self.add_log(self.__controller.lang_get('player_move_explan', values=(player.get_name(), piece[0], piece[1])))
        self.player_move_callback = callback
        
    player_remove_callback: callable
    def event_player_remove(self, player: Actor, callback: callable):
        print('event_player_remove', callback)
        self.add_log(self.__controller.lang_get('player_remove_explan', values=(player.get_name(),)))
        self.player_remove_callback = callback
    
        
            
