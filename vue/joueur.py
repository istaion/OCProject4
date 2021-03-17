#! /usr/bin/env python3
# coding: utf-8

import sys
sys.path.extend(["../controleurs"])

from functions import add_player, view_player, remove_player, change_ranking
from menu import menu

def player_menu():
    print("1: Liste des joueurs")
    print("2: ajouter un joueur")
    print("3: supprimer un joueur")
    print("4: changer les classement")
    print("5: retourner au menu principal")
    reponse = input()
    if reponse == "1":
        view_player()
        player_menu()
    elif reponse == "2":
        add_player()
        player_menu()
    elif reponse == "3":
        view_player()
        i=input("quel joueur voulez vous supprimer ? (saisissez le nombre) :")
        remove_player(i)
        player_menu()
    elif reponse == "4":
        change_ranking()
        player_menu()
    elif reponse == "5":
        menu()
    else:
        print("vous devez saisir un nombre entre 1 et 4")
        player_menu()
