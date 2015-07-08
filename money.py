#!/usr/bin/env python3

#  This file is part of OpenSoccerManager.
#
#  OpenSoccerManager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  OpenSoccerManager is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  OpenSoccerManager.  If not, see <http://www.gnu.org/licenses/>.


import math
import random

import calculator
import game
import news


def pay_bonus():
    '''
    Calculate the user-specified win bonus on the tactics screen.
    '''
    if game.clubs[game.teamid].tactics.win_bonus != 0:
        total = 0

        for playerid in game.clubs[game.teamid].team:
            if playerid != 0:
                total += game.players[playerid].wage

        bonus = total * (game.clubs[game.teamid].tactics.win_bonus * 0.1)
        game.clubs[game.teamid].accounts.withdraw(bonus, "playerwage")

        game.clubs[game.teamid].tactics.win_bonus = 0


def pay_win_bonus():
    '''
    Pay the win bonus amount defined within the players contract.
    '''
    for playerid in game.clubs[game.teamid].team.values():
        if playerid != 0:
            amount = game.players[playerid].bonus[2]
            game.clubs[game.teamid].accounts.withdraw(amount, "playerwage")


def prize_money(position):
    '''
    Handed out at end of season based on position, plus bonus for a
    first or second place finish.
    '''
    amount = 250000 * (21 - position)

    if position == 1:
        amount += 2500000
    elif position == 2:
        amount += 500000

    return amount


def flotation():
    '''
    Calculate estimated flotation amount for club.
    '''
    club = game.clubs[game.teamid]

    amount = club.reputation ** 2 * 100000

    form_affected = amount * 0.25
    amount -= form_affected

    points = 0
    form_length = len(club.form)

    if form_length > 12:
        form_length = 12

    for count in range(0, form_length):
        if club.form[count] == "W":
            points += 3
        elif club.form[count] == "D":
            points += 1

    if form_length >= 6:
        amount += (form_affected / form_length) * ((form_length * 3) - points)

    game.flotation.amount = amount


def float_club():
    '''
    Complete floating of club once timeout has been reached.
    '''
    if game.flotation.timeout > 0 and game.flotation.status == 1:
        game.flotation.timeout -= 1

        if game.flotation.timeout == 0:
            deposit(game.flotation.amount)
            game.news.publish("FL01")
