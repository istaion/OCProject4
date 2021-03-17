#! /usr/bin/env python3
# coding: utf-8

class Player:

    def __init__(self, nom, prenom, date_naissance, sexe, classement):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.classement = classement

    def __repr__(self):
        return(self.nom + " " + self.prenom)

    def __lt__(self, other):
        if self.classement < other.classement:
            return True
        else:
            return False

    def __le__(self, other):
        if self.classement <= other.classement:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.classement == other.classement:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.classement != other.classement:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.classement > other.classement:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.classement >= other.classement:
            return True
        else:
            return False
