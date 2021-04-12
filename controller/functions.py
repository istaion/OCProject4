#! /usr/bin/env python3
# coding: utf-8

import sys

sys.path.append("../model")

from tinydb import TinyDB, Query
from models import Player, Tournament, Round, Match
from datetime import datetime
from time import strftime


# Conversion between data base and models


def player_deserialize():
    """
    Function to put all players of the db.table in globals variables
    :return:
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    for item in players_table:
        globals()["player" + str(item.doc_id)] = Player(item["prenom"], item["nom"], item["date"], item["sexe"], item[
            "classement"], item.doc_id)


def player_serialize(player):
    """
    Function to update db.json
    :param player: player to update
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.update({"nom": player.last_name, "prenom": player.first_name, "date": player.birth_date,
                          "sexe": player.gender, "classement": player.ranking}, doc_ids=[player.id_json])


def tournament_deserialize():
    """
    Function to put all tournaments of the db.table in globals variables
    :return:
    """
    player_deserialize()
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    for item in tournament_table:
        players = []
        for player in item["players"]:  # to convert id's player in player object
            players.append((call_player(player[0]), player[1]))
        globals()["tournament" + str(item.doc_id)] = Tournament(item["name"], item["place"], item["date"], players,
                                                                item["time_control"], item["description"],
                                                                item["nb_round"], item["finish"])
        globals()["tournament" + str(item.doc_id)].end_date = item["end_date"]
        round_deserialize(globals()["tournament" + str(item.doc_id)])
        globals()["tournament" + str(item.doc_id)].rounds = []
        for i in range(item["round"]):  # to add rounds in the tournament list
            globals()["tournament" + str(item.doc_id)].rounds.append(globals()["round" + str(i + 1)])


def tournament_serialize(tournament):
    """
    Function to update db.json
    :param tournament: tournament to update
    """
    players = []
    for item in tournament.players:  # to convert player object in id
        players.append([item[0].id_json, item[1]])
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    query = Query()
    tournament_table.update({"place": tournament.place, "date": tournament.date, "end_date": tournament.end_date,
                             "round": tournament.active_round(),
                             "players": players, "time_control": tournament.time_control,
                             "description": tournament.descritpion, "nb_round": tournament.nb_round,
                             "finish": tournament.finish},
                            query.name == tournament.name)
    round_serialize(tournament)


def round_deserialize(tournament):
    """
    Function to put all round of a tournament in globals variables
    :param tournament: tournament to retrieve rounds
    """
    player_deserialize()
    db = TinyDB("db.json")
    round_table = db.table("rounds")
    query = Query()
    list_round = round_table.search(query.tournament == tournament.name)
    for item in list_round:
        globals()["round" + str(item["number"])] = Round(tournament.name,
                                                         Match(call_player(item["match1"][0][0]),
                                                               call_player(item["match1"][1][0]),
                                                               item["match1"][0][1], item["match1"][1][1],
                                                               item["match1"][2]),
                                                         Match(call_player(item["match2"][0][0]),
                                                               call_player(item["match2"][1][0]),
                                                               item["match2"][0][1], item["match2"][1][1],
                                                               item["match2"][2]),
                                                         Match(call_player(item["match3"][0][0]),
                                                               call_player(item["match3"][1][0]),
                                                               item["match3"][0][1], item["match3"][1][1],
                                                               item["match3"][2]),
                                                         Match(call_player(item["match4"][0][0]),
                                                               call_player(item["match4"][1][0]),
                                                               item["match4"][0][1], item["match4"][1][1],
                                                               item["match4"][2]),
                                                         item["status"])
        globals()["round" + str(item["number"])].date = item["date"]
        globals()["round" + str(item["number"])].end_date = item["end_date"]
        globals()["round" + str(item["number"])].match1.date = item["match1"][3]  # end date of match
        globals()["round" + str(item["number"])].match2.date = item["match2"][3]
        globals()["round" + str(item["number"])].match3.date = item["match3"][3]
        globals()["round" + str(item["number"])].match4.date = item["match4"][3]



def round_serialize(tournament):
    """
    Function to update rounds in the db.json
    :param tournament: tournament to retrieve rounds
    """
    player_deserialize()
    db = TinyDB("db.json")
    round_table = db.table("rounds")
    query = Query()
    for i, item in enumerate(tournament.rounds):
        round_table.update({"match1": [(item.match1.first_player.id_json, item.match1.first_player_score),
                                       (item.match1.second_player.id_json, item.match1.second_player_score),
                                       item.match1.resolved, item.match1.date],
                            "match2": [(item.match2.first_player.id_json, item.match2.first_player_score),
                                       (item.match2.second_player.id_json, item.match2.second_player_score),
                                       item.match2.resolved, item.match2.date],
                            "match3": [(item.match3.first_player.id_json, item.match3.first_player_score),
                                       (item.match3.second_player.id_json, item.match3.second_player_score),
                                       item.match3.resolved, item.match3.date],
                            "match4": [(item.match4.first_player.id_json, item.match4.first_player_score),
                                       (item.match4.second_player.id_json, item.match4.second_player_score),
                                       item.match4.resolved, item.match4.date],
                            "date": item.date, "end_date": item.end_date,
                            "status": item.status}, query.tournament == tournament.name and query.number == i + 1)


# functions to add an object in the data base

def round_add(turn, number):
    """
    Function to add round to db.json
    :param turn: round to add
    :param number: place of the round in the tournament
    """
    db = TinyDB("db.json")
    round_table = db.table("rounds")
    round_table.insert({"tournament": turn.tournament, "number": number,
                        "match1": [(turn.match1.first_player.id_json, turn.match1.first_player_score),
                                   (turn.match1.second_player.id_json, turn.match1.second_player_score),
                                   False, " "],
                        "match2": [(turn.match2.first_player.id_json, turn.match2.first_player_score),
                                   (turn.match2.second_player.id_json, turn.match2.second_player_score),
                                   False, " "],
                        "match3": [(turn.match3.first_player.id_json, turn.match3.first_player_score),
                                   (turn.match3.second_player.id_json, turn.match3.second_player_score),
                                   False, " "],
                        "match4": [(turn.match4.first_player.id_json, turn.match4.first_player_score),
                                   (turn.match4.second_player.id_json, turn.match4.second_player_score),
                                   False, " "],
                        "date": turn.date, "end_date": turn.end_date,
                        "status": False
                        })


def add_player(last_name, first_name, date, gender, ranking):  # A refaire pour mettre objet joueur en variable
    """
    function to add a new player in the db.json
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert({"nom": last_name, "prenom": first_name, "date": date, "sexe": gender, "classement": ranking})


def add_tournament(name, place, players, time_control, description, nb_round):  # A refaire pour mettre objet
                                                                                # tournoi en entrée
    """
    function to add a new player in the db.json
    """
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    if time_control == "1":
        time_control = "bullet"
    elif time_control == "2":
        time_control = "blitz"
    elif time_control == "3":
        time_control = "coup rapide"
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    tournament_table.insert({"name": name, "place": place, "date": date, "end_date": " ", "players": players, "round": 0,
                             "time_control": time_control, "description": description, "nb_round": nb_round,
                             "finish": False})

# Players functions


def change_player(i, last_name, first_name, date, gender):
    """
    function to change player's information
    :param i: id of the player in the db.table
    """
    player_deserialize()
    i = int(i)
    call_player(i).last_name = last_name
    call_player(i).first_name = first_name
    call_player(i).birth_date = date
    call_player(i).gender = gender
    player_serialize(call_player(i))


def change_ranking():
    """
    function to change all ranking
    :return:
    """
    player_deserialize()
    for i in range(number_player()):
        print(str(call_player(i + 1)) + " classement : " + str(call_player(i + 1).ranking))
        call_player(i + 1).ranking = input("nouveau classement :")
        player_serialize(call_player(i + 1))


def view_player():
    """
    :return: str with all players in the db.table
    """
    player_deserialize()
    players = ""
    for i in range(number_player()):
        players += str(i + 1) + ": " + str(call_player(i + 1)) + ", classement : " + str(
            call_player(i + 1).ranking) + "\n"
    return players


def call_player(i):
    """
    :param i: place of the player in the db.json
    :return: Player object
    """
    return globals()["player" + str(i)]


def number_player():
    """
    :return: Number of player in the db.json
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    return len(players_table)


# Tournament functions


def view_tournament():
    """
    function to view all tournament
    :return: str with all tournament
    """
    tournament_deserialize()
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    for i in range(len(tournament_table)):
        print("tournoi {} : {}".format(i + 1, globals()["tournament" + str(i + 1)]))


def new_round(i):
    """
    function to create a new round and 4 new match
    :param i: indice of the tournament in the db.json
    :return:
    """
    tournament_deserialize()
    tournament = globals()["tournament" + str(i)]
    player_deserialize()
    id_round = tournament.active_round()  # place of the last round (0 if there is not round)
    if id_round == 0:  # to create the first round
        player_list = []  # list of players in the tournament
        for player in tournament.players:
            player_list.append(player[0])
        player_list.sort()  # sort by ranking
        turn = Round(tournament.name, Match(player_list[0], player_list[4]), Match(player_list[1], player_list[5]),
                     Match(player_list[2], player_list[6]), Match(player_list[3], player_list[7]))
        turn.date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        round_add(turn, id_round + 1)
        tournament.rounds.append(turn)
        tournament_serialize(tournament)
    elif id_round <= tournament.nb_round:
        player_list = list(tournament.players)
        player_list.sort(key=lambda m: m[0])  # sort by ranking
        player_list.sort(reverse=True, key=lambda m: m[1])  # sort by score
        match = [[], [], [], []]  # list wish contain 4 matchs
        for n in range(4):  # take the first of the list, next take the second who haven't played against.
            match[n].append(player_list[0][0])
            stop = False
            for j in range(len(player_list) - 1):
                for i, turn in enumerate(tournament.rounds):
                    if turn.opponent(player_list[0][0], player_list[j + 1][0]):
                        break
                    elif i != id_round - 1:
                        continue
                    match[n].append(player_list[j + 1][0])  # store this players
                    player_list.pop(j + 1)
                    player_list.pop(0)  # suppress of the list for restart
                    stop = True
                if stop:
                    break
        turn = Round(tournament.name, Match(match[0][0], match[0][1]), Match(match[1][0], match[1][1]),
                     Match(match[2][0], match[2][1]), Match(match[3][0], match[3][1]))
        turn.date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        round_add(turn, id_round + 1)
        tournament.rounds.append(turn)
        tournament_serialize(tournament)
    else:
        print("erreur")


def continue_tournament(i):
    """
    check if the tournament is finish or if the active round is finish.
    if the active round is finish create a new round
    :param i: tournament id
    :return: str with the list of match to select the match to resolve
    """
    tournament_deserialize()
    tournament = globals()["tournament" + str(i)]
    if tournament.finish:
        res = "ce tournoi est fini"
    else:
        if tournament.active_round() == 0:
            new_round(i)
            tournament_deserialize()
            tournament = globals()["tournament" + str(i)]
        else:
            turn = tournament.rounds[-1]
            if turn.status:
                new_round(i)
                tournament_deserialize()
                tournament = globals()["tournament" + str(i)]
        turn = tournament.rounds[-1]
        res = ""
        for j, item in enumerate(turn.match_list()):
            res += str(j + 1) + ": " + str(item) + item.status() + "\n"
    return res


def resolve_match(i, j, k):
    """
    to resolve a match and add score of players
    :param i: tournament id
    :param j: match place
    :param k: 1 for first win, 2 for second win, 3 for ex aequo
    :return: str with the results of the match
    """
    tournament_deserialize()
    tournament = globals()["tournament" + str(i)]
    turn = tournament.rounds[-1]  # active round
    j = int(j) - 1
    k = int(k)
    turn.match_list()[j].resolve(k)
    turn.match_list()[j].date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    res = "le joueur " + str(turn.match_list()[j].first_player) + \
          " gagne " + str(turn.match_list()[j].first_player_score) + "points. \n" + \
          "le joueur " + str(turn.match_list()[j].second_player) + \
          " gagne " + str(turn.match_list()[j].second_player_score) + "points. \n"
    for indice, item in enumerate(turn.match_list()):
        if not item.resolved:
            break
        else:
            if indice == 3:
                turn.status = True
                tournament.update_score()
                turn.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                res += "Ce tour est fini \n"
                if tournament.nb_round == tournament.active_round():
                    tournament.finish = True
                    tournament.end_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    res += "Fin du tournoi"
    tournament_serialize(tournament)
    return res

# reports


def player_report(alphabetical=False):
    res = ""
    player_deserialize()
    player_list = []
    for i in range(number_player()):
        player_list.append(call_player(i+1))
    if alphabetical:
        player_list.sort(key=lambda m: m.last_name)
        for item in player_list:
            res += item.report() + "\n"
    else:
        player_list.sort()
        for item in player_list:
            res += item.report() + "\n"
    return res

