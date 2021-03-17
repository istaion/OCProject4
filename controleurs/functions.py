#! /usr/bin/env python3
# coding: utf-8

import sys
sys.path.append("../classe")

from tinydb import TinyDB, Query
from classes import Player


def add_player():
    db = TinyDB("db.json")
    players_table = db.table("players")

    nom = input("Nom de famille du joueur ? ")
    prenom = input("Prénom du joueur ? ")
    date = input("Date de naissance du joueur ? ")
    sexe = input("Sexe du joueur ? ")
    classement = input("Classement du joueur ? ")
    players_table.insert({"nom": nom, "prenom": prenom, "date": date, "sexe": sexe, "classement": classement})


def remove_player(i):
    i=int(i)
    db = TinyDB("db.json")
    players_table = db.table("players")
    query = Query()
    for idx, item in enumerate(players_table):
        if idx == i:
            players_table.remove(query.nom == item["nom"] and query.prenom == item["prenom"] and query.date == item["date"])
            break

def change_ranking():
    db = TinyDB("db.json")
    players_table = db.table("players")
    query = Query()
    for item in players_table:
        print(item["nom"] + " " + item["prenom"] + " classement actuel : " + item["classement"])
        rank = input("nouveau classement :")
        players_table.update({"classement": rank}, query.nom == item["nom"] and query.prenom == item["prenom"] and query.date == item["date"])

def view_player():
    db = TinyDB("db.json")
    players_table = db.table("players")
    for idx, item in enumerate(players_table):
        print("joueur" + str(idx) + " : " + item["nom"] + " " + item["prenom"] + " " + item["classement"])


def conversion():
    db = TinyDB("db.json")
    players_table = db.table("players")
    for idx, item in enumerate(players_table):
        globals()["player" + str(idx)] = Player(item["nom"], item["prenom"], item["date"], item["sexe"], item["classement"])


"""
    list_players = [player1, player2, player3, player4, player5, player6, player7, player8]
    list_players.sort()
    list1 = list_players[:int(len(list_players)/2)]
    list2 = list_players[int(len(list_players)/2):]
    print(list1, list2)"""
