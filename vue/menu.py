#! /usr/bin/env python3
# coding: utf-8

from joueur import player_menu

def menu():
    print("1: menu joueur")
    reponse = input()
    if reponse == "1":
        player_menu()