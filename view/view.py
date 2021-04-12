#! /usr/bin/env python3
# coding: utf-8

import sys

sys.path.extend(["../controller"])

from functions import *


def menu():
    print("1: menu joueur")
    print("2: menu tournoi")
    reponse = input()
    if reponse == "1":
        player_menu()
    elif reponse == "2":
        tournament_menu()


def player_menu():
    print("1: Liste des joueurs")
    print("2: ajouter un joueur")
    print("3: modifier les informations d'un joueur")
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
        i = input("quel joueur voulez vous modifier ? (saisissez le nombre) :")
        last_name = input("Nom de famille du joueur ? ")
        first_name = input("Prénom du joueur ? ")
        date = input("Date de naissance du joueur ? ")
        gender = input("Sexe du joueur ? ")
        change_player(i, last_name, first_name, date, gender)
        player_menu()
    elif reponse == "4":
        change_ranking()
        player_menu()
    elif reponse == "5":
        menu()
    else:
        print("vous devez saisir un entier entre 1 et 5")
        player_menu()

def tournament_menu():
    print("1: Créer un nouveau tournoi")
    print("2: Continuer un tournoi")
    reponse = input()
    if reponse == "1":
        name = input("nom du nouveau tournoi ? ")
        place = input("lieu du nouveau tournoi ? ")
        print("selectionner les 8 joueurs qui participeront à ce tournoi :")
        print(view_player())
        players = []
        for i in range(8):
            players.append([int(input("numéro du joueur :")), 0])
        nb_round = int(input("Nombre de tour du nouveau tournoi ? "))
        time_control = input("Contrôleur de temps ? Tapez 1 pour bullet, 2 pour blitz ou 3 pour coup rapide. ")
        description = input("Description du nouveau tournoi ? ")
        add_tournament(name, place, players, time_control, description, nb_round)
        tournament_menu()
    elif reponse == "2":
        print(view_tournament())
        i = input("Quel tournoi voulez vous continuer ? ")
        print(continue_tournament(i))
        j = input("Saisissez le numéro du match à résoudre :")
        k = input("Qui à gagné ? Taper 1 pour le premier joueur, 2 pour le deuxième, 3 pour ex aequo : ")
        print(resolve_match(i,j,k))
        tournament_menu()

