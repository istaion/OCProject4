#! /usr/bin/env python3
# coding: utf-8

from controller.functions import input_exception, view_player, add_player, number_player, change_player,\
    change_ranking, add_tournament, view_tournament, input_tournament_exception, continue_tournament,\
    input_match_exception, resolve_match, player_report, tournament_report, number_tournament,\
    player_tournament_report, round_tournament_report, active_tournament


def menu():
    print("1: menu joueur")
    print("2: menu tournoi")
    print("3: rapports")
    print("4: quitter le programme")
    reponse = input_exception(1, 4)
    if reponse == "1":
        player_menu()
    elif reponse == "2":
        tournament_menu()
    elif reponse == "3":
        report_menu()
    elif reponse == "4":
        exit()


def player_menu():
    print("1: Liste des joueurs")
    print("2: ajouter un joueur")
    print("3: modifier les informations d'un joueur")
    print("4: changer les classements")
    print("5: retourner au menu principal")
    reponse = input_exception(1, 5)
    if reponse == "1":
        print(view_player())
        player_menu()
    elif reponse == "2":
        last_name = input("Nom de famille du joueur ? ")
        first_name = input("Prénom du joueur ? ")
        date = input("Date de naissance du joueur ? ")
        gender = input("Sexe du joueur ? ")
        bo = True  # boolean = False when the input is correct
        while bo:  # check if the input is a int object
            try:
                ranking = input("Classement du joueur ? ")
                ranking = int(ranking)
                bo = False
            except ValueError:
                print("vous devez saisir un nombre entier")
        add_player(last_name, first_name, date, gender, ranking)  # add a player to the db.json
        player_menu()
    elif reponse == "3":
        print(view_player())
        print("quel joueur voulez vous modifier ? (saisissez le nombre) :")
        i = input_exception(1, number_player())
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


def tournament_menu():
    print("1: Créer un nouveau tournoi")
    print("2: Continuer un tournoi")
    print("3: Retourner au menu principal")
    reponse = input_exception(1, 3)
    if reponse == "1":
        name = input("nom du nouveau tournoi ? ")
        place = input("lieu du nouveau tournoi ? ")
        print("sélectionner les 8 joueurs qui participeront à ce tournoi :")
        print(view_player())
        new_players = []
        for i in range(8):
            bo = True  # boolean = False when the input is correct
            while bo:  # check if the input match with a player who has not already been selected
                try:
                    new = int(input("numéro du joueur :"))
                    assert new not in new_players
                    assert 0 <= new <= number_player()
                    new_players.append(new)
                    bo = False
                except AssertionError:
                    print("Ce joueur a déja été seléctionné ou n'existe pas.")
                except ValueError:
                    print("Vous devez saisir un nombre")
        players = []
        for item in new_players:
            players.append([item, 0])
        nb_round = int(input_exception(1, 7, "Nombre de tour du nouveau tournoi ? "))
        time_control = input_exception(1, 3, "Contrôleur de temps ? Tapez 1 pour bullet,"
                                             " 2 pour blitz ou 3 pour coup rapide. ")
        description = input("Description du nouveau tournoi ? ")
        add_tournament(name, place, players, time_control, description, nb_round)  # add tournament in the db.json
        tournament_menu()
    elif reponse == "2":
        if active_tournament():
            print(view_tournament(True))
            i = input_tournament_exception("Quel tournoi voulez vous continuer ? ")
            print(continue_tournament(i))  # eventually create a new round and print list of match
            j = input_match_exception(i, "Saisissez le numéro du match à résoudre :")
            k = input_exception(1, 3, "Qui à gagné ? Taper 1 pour le premier joueur,"
                                      " 2 pour le deuxième, 3 pour ex aequo : ")
            print(resolve_match(i, j, k))
            tournament_menu()
        else:
            print("Il n'y a pas de tournoi en cours, veuillez créer un nouveau tournoi.")
            tournament_menu()
    elif reponse == "3":
        menu()


def report_menu():
    print("1: liste des joueurs")
    print("2: liste des tournois")
    print("3: liste des joueurs d'un tournoi")
    print("4: liste des tours/matchs d'un tournoi")
    print("5: menu principal")
    reponse = input_exception(1, 5)
    if reponse == "1":
        print("1: par ordre alphébétique")
        print("2: par classement")
        reponse1 = input_exception(1, 2)
        if reponse1 == "1":
            print(player_report(True))  # True means in alphabetical order
            report_menu()
        elif reponse1 == "2":
            print(player_report())
            report_menu()
    elif reponse == "2":
        print(tournament_report())
        report_menu()
    elif reponse == "3":
        print(view_tournament())
        i = input_exception(1, number_tournament(), "De quel tournoi voulez vous voir les joueurs ? ")
        print("1: par classement ?")
        print("2: par ordre alphabétique ?")
        print("3: par score dans le tournoi ?")
        j = input_exception(1, 3)
        print(player_tournament_report(i, j))  # i : indice of the tournament, j : order, 1 for ranking,
        # 2 for alphabetical, 3 for score
        report_menu()
    elif reponse == "4":
        print(view_tournament())
        i = input_exception(1, number_tournament(), "De quel tournoi voulez vous voir les tours/matchs ? ")
        print("voulez vous le rapport :")
        print("1: des tours ?")
        print("2: des matchs ?")
        j = input_exception(1, 2)
        print(round_tournament_report(i, j))  # i : indice of the tournament, j : 1 for round, 2 for match
        report_menu()
    elif reponse == "5":
        menu()
