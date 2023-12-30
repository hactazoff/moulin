class Lang:
    
    default_lang = 'fr'
    
    def get(self, key: str, values: list[str] | None = [], lang: str | None = None) -> str:
        if lang is None:
            lang = self.default_lang
        text = langs.get(lang, {}).get(key, None)
        text = langs.get('fr', {}).get(key, None) if text is None else text
        text = langs.get('en', {}).get(key, None) if text is None else text
        if text is not None:
            for i in range(len(values)):
                text = text.replace('{' + str(i) + '}', str(values[i]))
        return f'[{key}]' if text is None else text
    
langs = {
    'fr': {
        'welcome': 'Bienvenue dans le jeu du Moulin !',
        'player_added': 'Le joueur {0} a été ajouté.',
        'player_removed': 'Le joueur {0} a été supprimé.',
        'start_game': 'Le jeu a lancé.',
        'player_win': 'Le joueur {0} a gagné.',
        'player_add_piece': 'Le joueur {0} a ajouté une pièce {1}.',
        'player_move_piece': 'Le joueur {0} a déplacé la pièce {1} en {2}.',
        'player_turn': 'C\'est au tour du joueur {0}.',
        'player_invalid_turn': 'Veuillez selectionner une pièce à déplacer/ajouter.',
        'player_invalid_move': 'Vous ne pouvez pas déplacer la pièce ici.',
        'player_turn_explan': 'Selectionnez une pièce à déplacer/ajouter.',
        'player_move_explan': 'Selectionnez une position pour déplacer la pièce.',
        'player_remove_explan': 'Selectionnez une pièce adverse à supprimer.',
        'player_invalid_remove': 'Veuillez selectionner une pièce adverse.',
        'player_eliminated': 'Le joueur {0} a été éliminé par le joueur {1}.',
        'player_loss_piece': 'Le joueur {0} a perdu une pièce en {1}. Il lui reste {2} pièces.',
    },
    'en': {}
}