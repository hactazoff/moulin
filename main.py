from src.actors.ai import AI
from src.actors.player import Player
from src.controller import Controller
from src.model import Model
from src.views.console import ViewConsole
from src.views.gui import ViewGUI
from src.constants import default_map, initial_max_pieces
import argparse

def main(args: argparse.Namespace):
    model = Model()
    if args.console:
        view = ViewConsole()
    else:
        view = ViewGUI()
    
    if args.map is None:
        model.set_map(default_map)
    else:
        with open(args.map, 'r') as f:
            model.set_map(f.readlines())

    controller = Controller(model, view)

    for i in range(args.player):
        player = Player(
            'Player ' + str(i + 1), 
            color=model.choise_color(), 
            max_pieces=initial_max_pieces
        )
        player.add_piece((i*2, i*2))
        controller.add_player(player)
        
    for i in range(args.ai):
        controller.add_player(AI(
            'AI ' + str(i + 1), 
            color=model.choise_color(), 
            max_pieces=initial_max_pieces
        ))

    controller.run()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--ai", type=int, help="Number of AI", default=0)
    parser.add_argument("-p", "--player", type=int, help="Number of players", default=2)
    parser.add_argument("-m", "--map", type=str, help="Map file path", default=None)
    parser.add_argument("-c", "--console", type=bool, help="Console mode", default=False)
    main(parser.parse_args())
