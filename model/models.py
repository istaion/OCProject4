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

    def new_round (self, new):
        self.rounds.append(new)


class Round:

    def __init__ (self, tournament, match1=[], match2=[], match3=[], match4=[]):
        self.tournament = tournament
        self.match1 = match1
        self.match2 = match2
        self.match3 = match3
        self.match4 = match4

    def __repr__ (self):
        return(str(self.match1) + str(self.match2) + str(self.match3) + str(self.match4))


    def opponent(self, player1, player2):
        reponse = False
        if self.match1[0][0] == player1.id_json or self.match1[1][0] == player1.id_json:
            if self.match1[0][0] == player2.id_json or self.match1[1][0] == player2.id_json:
                reponse = True
        elif self.match2[0][0] == player1.id_json or self.match2[1][0] == player1.id_json:
            if self.match2[0][0] == player2.id_json or self.match2[1][0] == player2.id_json:
                reponse = True
        elif self.match3[0][0] == player1.id_json or self.match3[1][0] == player1.id_json:
            if self.match3[0][0] == player2.id_json or self.match3[1][0] == player2.id_json:
                reponse = True
        elif self.match4[0][0] == player1.id_json or self.match4[1][0] == player1.id_json:
            if self.match4[0][0] == player2.id_json or self.match4[1][0] == player2.id_json:
                reponse = True
        return reponse

"""class Match:

    def __init__(self, (first_player, first_player_score), (second_player, second_player_score), resolved=False):
        self.first_player = first_player
        self.first_player_score = first_player_score
        self.second_player = second_player
        self.second_player_score = second_player_score
        self.resolved = resolved

    def resolve(self):
        pass
"""