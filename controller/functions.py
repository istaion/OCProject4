#! /usr/bin/env python3
# coding: utf-8

import sys
sys.path.append("../model")

from tinydb import TinyDB
from models import Player, Tournament, Round


def add_player(last_name, first_name, date, gender, ranking):
    """
    function to add a new player in the db.json
    :return:
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.insert({"nom": last_name, "prenom": first_name, "date": date, "sexe": gender, "classement": ranking})


def change_player(i, last_name, first_name, date, gender):
    """
    function to change player's informations in the db.json
    :param i: id of the player in the db.table
    :return:
    """
    i=int(i)
    db = TinyDB("db.json")
    players_table = db.table("players")
    players_table.update({"nom": last_name, "prenom": first_name, "date": date, "sexe": gender}, doc_ids=[i])


def change_ranking():
    """
    function to change all ranking
    :return:
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    for item in players_table:
        print(item["nom"] + " " + item["prenom"] + " classement actuel : " + item["classement"])
        rank = input("nouveau classement :")
        players_table.update({"classement": rank}, doc_ids = [item.doc_id])

def view_player():
    """
    :return: str with all players in the db.table
    """
    player_conversion()
    players = ""
    for i in range(number_player()):
        players += str(call_player(i+1)) + " classement : " + str(call_player(i+1).ranking) + "\n"
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

def player_conversion():
    """
    Function to put all players of the db.table in globals variables
    :return:
    """
    db = TinyDB("db.json")
    players_table = db.table("players")
    for item in players_table:
        globals()["player" + str(item.doc_id)] = Player(item["prenom"], item["nom"], item["date"], item["sexe"], item["classement"], item.doc_id)

def tournament_conversion():
    """
    Function to put all players of the db.table in globals variables
    :return:
    """
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    for item in tournament_table:
        globals()["tournament" + str(item.doc_id)] = Tournament(item["name"], item["place"], item["date"], item["players"], item["rounds"], item["time_control"], item["description"], item["nb_round"])

def add_tournament(name, place, date, players, time_control, description, nb_round):
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    if time_control == "1":
        time_control = "bullet"
    elif time_control == "2":
        time_control = "blitz"
    elif time_control == "3":
        time_control = "coup rapide"
    tournament_table.insert({"name": name, "place": place, "date": date, "players": players, "rounds": 1, "time_control": time_control, "description": description, "nb_round": nb_round})

def view_tournament():
    tournament_conversion()
    db = TinyDB("db.json")
    tournament_table = db.table("tournaments")
    for i in range(len(tournament_table)):
        print("tournoi {} : {}".format(i+1, globals()["tournament" + str(i+1)]))

def new_round(i):
    tournament_conversion()
    tournament = globals()["tournament" + str(i)]
    player_conversion()
    id_round = len(tournament.rounds)+1
    print(id_round)
    new_round = Round(tournament.name)
    player_list = []
    for player in tournament.players:
        player_list.append(call_player(player[0]))
    player_list.sort()
    print(player_list)
    new_round.match1 = [[player_list[0].id_json,0],[player_list[4].id_json,0]]
    new_round.match2 = [[player_list[1].id_json,0],[player_list[5].id_json,0]]
    new_round.match3 = [[player_list[2].id_json,0],[player_list[6].id_json,0]]
    new_round.match4 = [[player_list[3].id_json,0],[player_list[7].id_json,0]]
    print(new_round)
    db = TinyDB("db.json")
    round_table = db.table("rounds")
    round_table.insert({"tournament": new_round.tournament, "number": id_round, "match1": new_round.match1,  "match2": new_round.match2, "match3": new_round.match3, "match4": new_round.match4})