# Maze-game

## Description

Minotaur Maze Game est un jeu de labyrinthe où le joueur doit échapper au Minotaure et atteindre la sortie. Le jeu est développé en Python en utilisant la bibliothèque Pygame pour le rendu graphique et NetworkX pour la gestion du graphe du labyrinthe.

## Fonctionnalités

- Génération aléatoire de labyrinthes de différentes tailles et difficultés.
- Mouvements du joueur et du Minotaure.
- Conditions de victoire et de défaite.
- Menu principal avec options pour jouer, afficher les contrôles et quitter le jeu.
- Interface utilisateur intuitive.

## Installation

### Prérequis

- Python 3.x
- Pygame
- NetworkX
- Requests

### Étapes d'installation

1. Clonez le dépôt :

    ```sh
    git clone https://github.com/votre-utilisateur/minotaur-maze-game.git
    ```

2. Installez les dépendances :

    ```sh
    pip install -r requirements.txt
    ```

## Utilisation

### Lancer le jeu

Pour lancer le jeu, exécutez le fichier principal `main.py` :

```sh
python main.py
Options de ligne de commande
Vous pouvez spécifier la taille et la difficulté du labyrinthe en utilisant des arguments de ligne de commande (par défaut c'est random) :

size : Taille du labyrinthe (small, medium, large, random).
difficulty : Difficulté du labyrinthe (easy, medium, hard, random).
Exemples :


python main.py medium hard

Contrôles
Monter : Z ou Flèche Haut
Descendre : S ou Flèche Bas
Gauche : Q ou Flèche Gauche
Droite : D ou Flèche Droite
Passer : Espace
Réinitialiser : Retour Arrière
Annuler : Maj
