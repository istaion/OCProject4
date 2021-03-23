#! /usr/bin/env python3
# coding: utf-8

class Player:

    def __init__ (self, first_name, last_name, birth_date, gender, ranking, id_json):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.ranking = ranking
        self.id_json = id_json

    def __repr__ (self):
        return (self.first_name + " " + self.last_name)

    def __lt__ (self, other):
        if self.ranking < other.ranking:
            return True
        else:
            return False

    def __le__ (self, other):
        if self.ranking <= other.ranking:
            return True
        else:
            return False

    def __eq__ (self, other):
        if self.ranking == other.ranking:
            return True
        else:
            return False

    def __ne__ (self, other):
        if self.ranking != other.ranking:
            return True
        else:
            return False

    def __gt__ (self, other):
        if self.ranking > other.ranking:
            return True
        else:
            return False

    def __ge__ (self, other):
        if self.ranking >= other.ranking:
            return True
        else:
            return False


class Tournament:

    def __init__ (self, name, place, date, players, rounds, time_control, description, nb_round=4, finish=False):
        self.name = name
        self.place = place
        self.date = date
        self.players = players
        self.rounds = rounds
        self.time_control = time_control
        self.descritpion = description
        self.nb_round = nb_round
        self.finish = finish

    def __repr__ (self):
        return (self.name)

    def new_round (self):
        if len(self.rounds) == 0:


class Round:

    def __init__ (self, tournament):
        self.tournament = tournament
        self.match1 = []
        self.match2 = []
        self.match3 = []
        self.match4 = []


    def __repr__ (self):
        return(str(self.match1) + str(self.match2) + str(self.match3) + str(self.match4))