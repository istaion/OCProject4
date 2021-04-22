#! /usr/bin/env python3
# coding: utf-8

class Player:

    def __init__(self, first_name, last_name, birth_date, gender, ranking, id_json):
        self.first_name = first_name.capitalize()  # str
        self.last_name = last_name.capitalize()  # str
        self.birth_date = birth_date  # str
        self.gender = gender  # str
        self.ranking = ranking  # int
        self.id_json = id_json  # int, id of player in the json file

    def __repr__(self):
        return self.last_name + " " + self.first_name

    def report(self):
        """
        :return: str with all player's information
        """
        return self.last_name + " " + self.first_name + ", classement: " + str(self.ranking) +\
            ", date de naissance: " + self.birth_date + ", genre: " + self.gender

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
        self.end_date = " "

    def report(self):
        """
        :return: str with all tournament informations (except players and matchs)
        """
        if self.finish:
            return "tournoi: " + self.name + ", status: fini, date de début: " + self.date\
                   + ", date de fin: " + self.end_date + ", lieu: " + self.place\
                   + ", contrôle du temps: " + self.time_control + ", nombre de round: " + str(self.nb_round) \
                   + "\n" + "         description: " + self.descritpion + "\n"
        else:
            return "tournoi: " + self.name + ", status: en cours, date de début: " + self.date +\
                   ", lieu: " + self.place + ", contrôle du temps: " + self.time_control +\
                   ", nombre de round: " + str(self.nb_round) + "\n" + "\t description: " + self.descritpion + "\n"

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

    def new_round(self, new):
        """
        add a round in the round list
        :param new: round to add
        :return:
        """
        self.rounds.append(new)


class Round:

    def __init__(self, tournament, match1, match2, match3, match4, status=False):
        self.tournament = tournament  # str, name of the tournament's round
        self.number = 0  # number of this round
        self.match1 = match1  # Match objet
        self.match2 = match2
        self.match3 = match3
        self.match4 = match4
        self.status = status  # boolean to control if the round is finished
        self.date = " "
        self.end_date = " "

    def __repr__(self):
        return "match1 : " + str(self.match1) + " match2 : " \
               + str(self.match2) + " match3 : " + str(self.match3) + " match4 : " + str(self.match4)

    def report(self):
        if self.status:
            return "tour" + str(self.number) + ": " + ", date de début: " + \
                   self.date + ", date de fin: " + self.end_date + "\n \t match1 : " + str(self.match1) +\
                   "\n \t match2 : " + str(self.match2) + "\n \t match3 : " +\
                   str(self.match3) + "\n \t match4 : " + str(self.match4) + "\n"
        else:
            return "tour" + str(self.number) + ": " + str(self) + ", date de début: " + \
                   self.date + ", ce match n'est pas fini." + "\n \t match1 : " + str(self.match1) +\
                   "\n \t match2 : " + str(self.match2) + "\n \t match3 : " +\
                   str(self.match3) + "\n \t match4 : " + str(self.match4) + "\n"

    def opponent(self, player1, player2):
        """
        controll if 2 players have already played against each other
        :param player1: Player object
        :param player2: Player object
        :return: if they already played : True, else : False
        """
        response = False
        player1 = player1.id_json
        player2 = player2.id_json
        for item in self.match_list():
            if item.first_player.id_json == player1 or item.second_player.id_json == player1:
                if item.first_player.id_json == player2 or item.second_player.id_json == player2:
                    response = True
        return response

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

    def __init__(self, first_player, second_player, first_player_score=0, second_player_score=0,
                 resolved="in progress"):
        self.first_player = first_player  # Player object
        self.first_player_score = first_player_score  # int
        self.second_player = second_player
        self.second_player_score = second_player_score
        self.resolved = resolved  # in progress, first_win, second_win, ex_aequo
        self.date = " "

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
