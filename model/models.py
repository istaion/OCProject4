#! /usr/bin/env python3
# coding: utf-8

class Player:

    def __init__(self, first_name, last_name, birth_date, gender, ranking, id_json):
        self.first_name = first_name  # str
        self.last_name = last_name  # str
        self.birth_date = birth_date  # str
        self.gender = gender  # str
        self.ranking = ranking  # int
        self.id_json = id_json  # int, id of player in the json file

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def __lt__(self, other):
        if self.ranking < other.ranking:
            return True
        else:
            return False

    def __le__(self, other):
        if self.ranking <= other.ranking:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.ranking == other.ranking:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.ranking != other.ranking:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.ranking > other.ranking:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.ranking >= other.ranking:
            return True
        else:
            return False


class Tournament:

    def __init__(self, name, place, date, players, time_control, description, nb_round=4, finish=False, rounds=[]):
        self.name = name  # str
        self.place = place  # str
        self.date = date  # str
        self.players = players  # list of tuple : (player object, score of the player)
        self.time_control = time_control  # "bullet", "blitz" or "coup rapide"
        self.descritpion = description  # str
        self.nb_round = nb_round  # int, number of rounds in the tournament
        self.finish = finish  # boolean to control if the tournament is finished
        self.rounds = rounds  # list of round

    def active_round(self):
        """
        :return: number of actual round
        """
        return len(self.rounds)

    def update_score(self):
        """
        ad score of the actual round to players list
        """
        new_list = []
        turn = self.rounds[-1]
        for player in self.players:
            new_list.append((player[0], player[1] + turn.score(player[0])))
        self.players = new_list

    def __repr__(self):
        return self.name

    def new_round (self, new):
        """
        add a round in the round list
        :param new: round to add
        :return:
        """
        self.rounds.append(new)


class Round:

    def __init__(self, tournament, match1, match2, match3, match4, status=False):
        self.tournament = tournament  # str, name of the tournament's round
        self.match1 = match1  # Match objet
        self.match2 = match2
        self.match3 = match3
        self.match4 = match4
        self.status = status  # boolean to control if the round is finished

    def __repr__(self):
        return "match1 : " + str(self.match1) + " match2 : " \
               + str(self.match2) + " match3 : " + str(self.match3) + " match4 : " + str(self.match4)

    def opponent(self, player1, player2):  # A refaire (rajouter une boucle)
        """
        controll if 2 players have already played against each other
        :param player1: Player object
        :param player2: Player object
        :return: if they already played : True, else : False
        """
        reponse = False
        player1 = player1.id_json
        player2 = player2.id_json
        if self.match1.first_player.id_json == player1 or self.match1.second_player.id_json == player1:
            if self.match1.first_player.id_json == player2 or self.match1.second_player.id_json == player2:
                reponse = True
        elif self.match2.first_player.id_json == player1 or self.match2.second_player.id_json == player1:
            if self.match2.first_player.id_json == player2 or self.match2.second_player.id_json == player2:
                reponse = True
        elif self.match3.first_player.id_json == player1 or self.match3.second_player.id_json == player1:
            if self.match3.first_player.id_json == player2 or self.match3.second_player.id_json == player2:
                reponse = True
        elif self.match4.first_player.id_json == player1 or self.match4.second_player.id_json == player1:
            if self.match4.first_player.id_json == player2 or self.match4.second_player.id_json == player2:
                reponse = True
        return reponse

    def score(self, player):
        """
        :param player: Player object
        :return: score of the player in this round
        """
        player = player.id_json
        for item in self.match_list():
            if item.first_player.id_json == player:
                return item.first_player_score
            elif item.second_player.id_json == player:
                return item.second_player_score

    def match_list(self):
        """
        :return: a list with all match
        """
        return [self.match1, self.match2, self.match3, self.match4]


class Match:

    def __init__(self, first_player, second_player, first_player_score=0, second_player_score=0, resolved=False):
        self.first_player = first_player  # Player object
        self.first_player_score = first_player_score  # int
        self.second_player = second_player
        self.second_player_score = second_player_score
        self.resolved = resolved  # False, first_win, second_win, ex_aequo

    def __repr__(self):
        return str(self.first_player) + " versus " + str(self.second_player)

    def status(self):
        """
        :return: str to describe status of the match (non resolved, first_win, second win or ex aequo)
        """
        if self.resolved == "first_win":
            return " gagnant : " + str(self.first_player)
        elif self.resolved == "second_win":
            return " gagnant : " + str(self.second_player)
        elif self.resolved == " ex_aequo":
            return self.resolved
        else:
            return " résultats en attente"

    def resolve(self, i):
        """
        to change status of the match and add score to player
        :param i: int (1 for first win, 2 for second win, 3 for ex aequo)
        """
        if i == 1:
            self.first_player_score = 1
            self.resolved = "first_win"
        elif i == 2:
            self.second_player_score = 1
            self.resolved = "second_win"
        elif i == 3:
            self.first_player_score = 0.5
            self.second_player_score = 0.5
            self.resolved = " ex_aequo"
