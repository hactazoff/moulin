# Moulin Game

Le jeu du moulin est un jeu de plateau pour deux joueurs. Chaque joueur dispose de 9 pions qu'il doit placer sur le plateau. Une fois les pions placés, les joueurs doivent les déplacer sur les intersections du plateau. Le but du jeu est de former un moulin, c'est-à-dire aligner trois pions sur une même ligne. Lorsqu'un moulin est formé, le joueur peut retirer un pion adverse du plateau. Le premier joueur qui ne peut plus jouer a perdu.

## Installation

Pour installer le jeu, il suffit de cloner le dépôt git et de lancer le script d'installation.
```bash
git clone https://github.com/hactazoff/moulin
cd moulin
```

> Si vous utilisez sur windows, vous pouvez télécharger la dépendance [Sun-Valley-ttk-theme](https://github.com/rdbende/Sun-Valley-ttk-theme) avec pip.
> ```bash
> pip install sv-ttk
> ```

## Utilisation

Pour lancer le jeu, il suffit de lancer le script `moulin.py`.
```bash
python moulin.py
```

Plusieurs options sont disponibles :
- `-h` ou `--help` : affiche l'aide
- `-p` ou `--player [int]` : permet de choisir le nombre de joueurs

Ces options ne sont pas encore implémentées :
- `-c` ou `--console [bool]` : permet de lancer le jeu en mode console
- `-a` ou `--ai [int]` : permet de lancer le jeu en mode joueur contre IA
- `-m` ou `--map [str]` : permet de choisir la carte du jeu depuis un fichier