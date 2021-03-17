#! /usr/bin/env python3
# coding: utf-8

import sys
sys.path.append("./vue")
sys.path.append("./controleurs")
sys.path.append("./classe")

from functions import conversion
from vue import menu, player_menu


def main():
    conversion()
    menu()



if __name__ == "__main__":
    main()