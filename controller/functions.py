#! /usr/bin/env python3
# coding: utf-8

import sys

sys.path.append("../model")

from tinydb import TinyDB, Query
from models import Player, Tournament, Round


def add_player (last_name, first_name, date, gender, ranking):
    """
    function to add a new player in the db.json
    :return:
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert({"nom": last_name, "prenom": first_name, "date": date, "sexe": gender, "classement": ranking})


def change_player (i, last_name, first_name, date, gender):
    """
    function to change player's informations in the db.json
    :param gender:
    :param date:
    :param first_name:
    :param last_name:
    :param i: id of the player in the db.table
    :return:
    """
    player_deserialize()
    i = int(i)
    call_player(i).last_name = last_name
    call_player(i).first_name = first_name
    call_player(i).birth_date = date
    call_player(i).gender = gender
    player_serialize(call_player(i))


def change_ranking ():
    """
    function to change all ranking
    :return:
    """
    player_deserialize()
    for i in range(number_player()):
        print(str(call_player(i + 1)) + " classement : " + str(call_player(i + 1).ranking))
        call_player(i + 1).ranking = input("nouveau classement :")
        player_serialize(call_player(i + 1))


def view_player ():
    """
    :return: str with all players in the db.table
    """
    player_deserialize()
    players = ""
    for i in range(number_player()):
        players += str(i + 1) + ": " + str(call_player(i + 1)) + ", classement : " + str(
            call_player(i + 1).ranking) + "\n"
    return players


def call_player (i):
    """
    :param i: place of the player in the db.json
    :return: Player object
    """
    return globals()["player" + str(i)]


def number_player ():
    """
    :return: Number of player in the db.json
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    return len(players_table)


def player_deserialize ():
    """
    Function to put all players of the db.table in globals variables
    :return:
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    for item in players_table:
        globals()["player" + str(item.doc_id)] = Player(item["prenom"], item["nom"], item["date"], item["sexe"], item[
            "classement"], item.doc_id)


def player_serialize (player):
    """
    Function to update db.json
    :param player: player to update
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.update({"nom": player.last_name, "prenom": player.first_name, "date": player.birth_date,
                          "sexe": player.gender, "classement": player.ranking}, doc_ids=[player.id_json])


def tournament_serialize (tournament):
    """
    Function to update db.json
    :param tournament: tournament to update
    """
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    query = Query()
    tournament_table.update({"rounds": tournament.rounds}, query.name == tournament.name)


def tournament_deserialize ():
    """
    Function to put all tournaments of the db.table in globals variables
    :return:
    """
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    for item in tournament_table:
        globals()["tournament" + str(item.doc_id)] = Tournament(item["name"], item["place"], item["date"], item[
            "players"], item["rounds"], item["time_control"], item["description"], item["nb_round"])


def round_deserialize (tournament):
    """
    Function to put all round of a tournament in globals variables
    :param tournament: tournament to retrieve rounds
    """
    db = TinyDB("db.json")
    round_table = db.table("rounds")
    query = Query()
    list_round = round_table.search(query.tournament == tournament.name)
    for item in list_round:
        globals()["round" + str(item["number"])] = Round(tournament.name, item["match1"], item["match2"],
                                                         item["match3"], item["match4"])


def round_add (turn, number):
    """
    Function to add round to db.json
    :param turn: round to add
    :param number: place of the round in the tournament
    """
    db = TinyDB("db.json")
    round_table = db.table("rounds")
    round_table.insert({"tournament": turn.tournament, "number": number, "match1": turn.match1, "match2": turn.match2,
                        "match3": turn.match3, "match4": turn.match4})


def add_tournament (name, place, date, players, time_control, description, nb_round):
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    if time_control == "1":
        time_control = "bullet"
    elif time_control == "2":
        time_control = "blitz"
    elif time_control == "3":
        time_control = "coup rapide"
    tournament_table.insert({"name": name, "place": place, "date": date, "players": players, "rounds": (0, False),
                             "time_control": time_control, "description": description, "nb_round": nb_round})


def view_tournament ():
    tournament_deserialize()
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    for i in range(len(tournament_table)):
        print("tournoi {} : {}".format(i + 1, globals()["tournament" + str(i + 1)]))


def new_round (i):
    tournament_deserialize()
    tournament = globals()["tournament" + str(i)]
    player_deserialize()
    id_round = tournament.rounds[0]
    if id_round == 0:
        turn = Round(tournament.name)
        player_list = []
        for player in tournament.players:
            player_list.append(call_player(player[0]))
        player_list.sort()
        turn.match1 = [[player_list[0].id_json, 0], [player_list[4].id_json, 0]]
        turn.match2 = [[player_list[1].id_json, 0], [player_list[5].id_json, 0]]
        turn.match3 = [[player_list[2].id_json, 0], [player_list[6].id_json, 0]]
        turn.match4 = [[player_list[3].id_json, 0], [player_list[7].id_json, 0]]
        round_add(turn, id_round + 1)
        tournament.rounds = (1, False)
        tournament_serialize(tournament)
    elif id_round <= tournament.nb_round:
        turn = Round(tournament.name)
        player_list = []
        for player in tournament.players:
            player_list.append([call_player(player[0]), player[1]])
        player_list.sort(key=lambda m: m[0])  # On commence par trier selon le classement
        player_list.sort(reverse=True, key=lambda m: m[1])  # Puis selon le score
        round_deserialize(tournament)
        turn.match1 = [[player_list[0][0].id_json, player_list[0][1]]]
        stop = False
        for j in range(len(player_list)-1):
            for i in range(id_round):
                if globals()["round" + str(i+1)].opponent(player_list[0][0],player_list[j+1][0]):
                    break
                elif i != id_round-1:
                    continue
                turn.match1.append([player_list[j+1][0].id_json, player_list[j+1][1]])
                player_list.pop(j+1)
                player_list.pop(0)
                stop = True
                print(turn.match1)
                print(player_list)
            if stop:
                break
        turn.match2 = [[player_list[0][0].id_json, player_list[0][1]]]
        stop = False
        for j in range(len(player_list)-1):
            for i in range(id_round):
                if globals()["round" + str(i+1)].opponent(player_list[0][0],player_list[j+1][0]):
                    break
                elif i != id_round-1:
                    continue
                turn.match2.append([player_list[j+1][0].id_json, player_list[j+1][1]])
                player_list.pop(j+1)
                player_list.pop(0)
                stop = True
                print(turn.match2)
                print(player_list)
            if stop:
                break
        turn.match3 = [[player_list[0][0].id_json, player_list[0][1]]]
        stop = False
        for j in range(len(player_list)-1):
            for i in range(id_round):
                if globals()["round" + str(i+1)].opponent(player_list[0][0],player_list[j+1][0]):
                    break
                elif i != id_round-1:
                    continue
                turn.match3.append([player_list[j+1][0].id_json, player_list[j+1][1]])
                player_list.pop(j+1)
                player_list.pop(0)
                stop = True
                print(turn.match3)
                print(player_list)
            if stop:
                break

        turn.match4 = [[player_list[0][0].id_json, player_list[0][1]], [player_list[1][0].id_json, player_list[1][1]]]
        print(turn.match4)
        print(turn)
        round_add(turn, id_round + 1)
        tournament.rounds = (id_round + 1, False)
        tournament_serialize(tournament)
    else:
        print("erreur")
