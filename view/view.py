#! /usr/bin/env python3
# coding: utf-8

import sys

sys.path.extend(["../controller"])

from functions import add_player, view_player, remove_player, change_ranking


def menu():
    print("1: menu joueur")
    reponse = input()
    if reponse == "1":
        player_menu()


def player_menu():
    print("1: Liste des joueurs")
    print("2: ajouter un joueur")
    print("3: supprimer un joueur")
    print("4: changer les classements")
    print("5: retourner au menu principal")
    reponse = input()
    if reponse == "1":
        print(view_player())
        player_menu()
    elif reponse == "2":
        last_name = input("Nom de famille du joueur ? ")
        first_name = input("Prénom du joueur ? ")
        date = input("Date de naissance du joueur ? ")
        gender = input("Sexe du joueur ? ")
        ranking = input("Classement du joueur ? ")
        add_player(last_name, first_name, date, gender, ranking)
        player_menu()
    elif reponse == "3":
        print(view_player())
        i = input("quel joueur voulez vous supprimer ? (saisissez le nombre) :")
        remove_player(i)
        player_menu()
    elif reponse == "4":
        change_ranking()
        player_menu()
    elif reponse == "5":
        menu()
    else:
        print("vous devez saisir un entier entre 1 et 5")
        player_menu()
