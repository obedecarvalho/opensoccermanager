#!/usr/bin/env python3

import game


def morale(playerid, amount):
    '''
    Specify adjustment for player morale.
    '''
    player = game.players[playerid]
    player.morale += amount

    if player.morale > 100:
        player.morale = 100
    elif player.morale < -100:
        player.morale = -100


def update():
    '''
    Update all evaluation value categories.
    '''
    club = game.clubs[game.teamid]

    # Fans
    points = 0

    for item in club.form:
        if item == "W":
            points += 3
        elif item == "D":
            points += 1

    if len(club.form) > 0:
        percentage = points / (len(club.form) * 3) * 100
    else:
        percentage = 0

    percentage = int(percentage)

    club.evaluation[1] = percentage

    # Finances
    total = (club.reputation ** 3 * 1000 * 3) * 2
    percentage = (club.balance / total) * 100

    if percentage > 100:
        percentage = 100

    club.evaluation[2] = percentage

    # Players
    points = 0

    for playerid in club.squad:
        player = game.players[playerid]
        points += player.morale

    maximum = len(club.squad) * 100
    total = maximum * 2

    percentage = ((points + maximum) / total) * 100

    club.evaluation[3] = percentage

    # Staff
    if len(club.coaches_hired) + len(club.scouts_hired) > 0:
        points = 0

        for coachid, coach in club.coaches_hired.items():
            points += coach.morale

        for scoutid, scout in club.scouts_hired.items():
            points += scout.morale

        maximum = (len(club.coaches_hired) + len(club.scouts_hired)) * 10
        percentage = (points / maximum) * 100

        club.evaluation[4] = percentage

    # Chairman
    subtotal = sum(club.evaluation[1:])

    if len(club.coaches_hired) + len(club.scouts_hired) > 0:
        percentage = (subtotal / 400) * 100
    else:
        percentage = (subtotal / 300) * 100

    percentage = int(percentage)

    club.evaluation[0] = percentage


def indexer(index):
    '''
    Determine appropriate message to display for each evaluation item.
    '''
    if index < 10:
        value = 0
    elif 10 <= index < 25:
        value = 1
    elif 25 <= index < 40:
        value = 2
    elif 40 <= index < 55:
        value = 3
    elif 55 <= index < 70:
        value = 4
    elif 70 <= index < 85:
        value = 5
    elif index >= 85:
        value = 6

    return value


def calculate_overall():
    '''
    Calculate overall evaluation percentage.
    '''
    club = game.clubs[game.teamid]

    if club.evaluation[4] == 0:
        multiplier = 0.25
    else:
        multiplier = 0.2

    total = sum(club.evaluation) * multiplier

    return total
