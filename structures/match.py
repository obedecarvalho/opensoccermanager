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


import random

import data


class Team:
    def __init__(self, fixture):
        self.fixture = fixture

    def set_team_selection(self):
        '''
        Set team selection for match into fixture object.
        '''
        club = self.fixture.home.club
        self.fixture.home.team_selection[0] = club.squad.teamselection.team
        self.fixture.home.team_selection[1] = club.squad.teamselection.subs

        club = self.fixture.away.club
        self.fixture.away.team_selection[0] = club.squad.teamselection.team
        self.fixture.away.team_selection[1] = club.squad.teamselection.subs


class Score:
    def __init__(self, fixture):
        self.fixture = fixture

        self.calculate_skills()

    def calculate_skills(self):
        '''
        Calculate player scores for team selection from skill attributes.
        '''
        self.weights = [1, 1] #0, 0

        for count, club in enumerate((self.fixture.home.club,
                                      self.fixture.away.club)):
            for player in club.squad.teamselection.team:
                if player:
                    self.weights[count] = sum(player.get_skills())

        self.total = sum(self.weights)

        self.calculate_percentages()

    def home_advantage(self):
        '''
        Determine home advantage score based on form and fan morale.
        '''
        points = 0

        for item in self.fixture.home.club.form.get_form_for_length(6):
            if item == "W":
                points += 3
            elif item == "D":
                points += 1
            elif item == "L":
                points -= 1

        return points

    def calculate_percentages(self):
        '''
        Determine percentage chance of win, loss, and draw for each team.
        '''
        percent1 = ((self.weights[0] / self.total) + self.home_advantage()) * 100
        percent1 = (percent1 * 0.05) * self.fixture.home.club.reputation
        self.percent1 = round(percent1)

        percent2 = (self.weights[0] / self.total) * 100
        percent2 = (percent2 * 0.05) * self.fixture.away.club.reputation
        self.percent2 = round(percent2)

        self.determine_result()

    def determine_result(self):
        '''
        Produce final result for match.
        '''
        if self.percent1 > self.percent2:
            draw = self.percent1 - self.percent2
        elif self.percent1 < self.percent2:
            draw = self.percent2 - self.percent1
        else:
            draw = 0

        ranges = [[], [], []]
        ranges[0] = [0, self.percent1]
        ranges[1] = [ranges[0][1], self.percent1 + draw]
        ranges[2] = [ranges[1][1], ranges[1][1] + self.percent2]

        if ranges == [[0, 0], [0, 0], [0, 0]]:
            ranges = [[1, 2], [3, 4], [5, 6]]

        [list(map(int, item)) for item in ranges]

        choice = random.randrange(0, int(ranges[2][1]))

        if choice < ranges[0][1]:
            score = self.generate_goals()
        elif choice < ranges[1][1]:
            score = self.generate_goals()
            score = score[0], score[0]
        elif choice < ranges[2][1]:
            score = self.generate_goals()
            score = score[1], score[0]

        self.fixture.result = score

        substitutes = Substitutes(self.fixture.home)
        substitutes.generate_substitutes()

        injuries = Injuries(self.fixture.home)
        injuries.generate_injuries()

        substitutes = Substitutes(self.fixture.away)
        substitutes.generate_substitutes()

        injuries = Injuries(self.fixture.away)
        injuries.generate_injuries()

        goalscorers = Goalscorers(self.fixture.home.club, score[0])
        self.fixture.home.goalscorers = goalscorers.generate_goalscorers()

        goalscorers = Goalscorers(self.fixture.away.club, score[1])
        self.fixture.away.goalscorers = goalscorers.generate_goalscorers()

    def generate_goals(self):
        '''
        Generate goals scored for both teams.
        '''
        score1 = 1

        club = self.fixture.home.club

        if club.tactics.playing_style == 0:
            start = 35
        elif club.tactics.playing_style == 1:
            start = 50
        elif club.tactics.playing_style == 2:
            start = 65

        for x in range(2, 9):
            if random.randint(0, 100) < start:
                score1 += 1
                start = int(start * 0.5)

                if start < 1:
                    start = 1

        score2 = random.randint(0, score1 - 1)

        return score1, score2


class Substitutes:
    def __init__(self, fixtureteam):
        self.fixtureteam = fixtureteam

    def generate_substitutes(self):
        if len(self.fixtureteam.club.squad.teamselection.subs) >= 3:
            choice = random.randint(0, 3)
        else:
            choice = random.randint(0, len(self.fixtureteam.club.squad.teamselection.subs))

        substitutes = [player for player in self.fixtureteam.club.squad.teamselection.subs]
        selected = []

        for count in range(0, choice):
            player = substitutes[count]
            selected.append(player)
            substitutes.remove(player)

        self.fixtureteam.team_played[1] = selected


class Goalscorers:
    def __init__(self, club, score):
        self.club = club
        self.score = score

    def calculate_score(self, player):
        '''
        Determine chance of goalscorer.
        '''
        maximum = 0

        if player.position == "GK":
            maximum = 1
        elif player.position in ("DL", "DR", "DC", "D"):
            maximum = player.tackling
        elif player.position in ("ML", "MR", "MC", "M"):
            maximum = player.passing * 2.5
        elif player.position in ("AS", "AF"):
            maximum = player.shooting * 5

        return maximum

    def generate_goalscorers(self):
        '''
        Return goalscorer object for goals.
        '''
        if self.score > 0:
            goalscorers = []

            for count in range(0, self.score):
                scores = []

                for player in self.club.squad.teamselection.get_team_selection():
                    if player:
                        maximum = self.calculate_score(player)

                        for count in range(0, int(maximum)):
                            scores.append(player)

                random.shuffle(scores)

                goalscorer = random.choice(scores)
                goalscorers.append(goalscorer)

            return goalscorers

        return None


class Assisters:
    def __init__(self, club):
        self.club = club

    def get_assister(self, goalscorer):
        '''
        Get assister for passed goalscorer.
        '''
        players = [player for player in self.club.squad.teamselection.get_team_selection() if player]

        return random.choice(players)


class Injuries:
    def __init__(self, fixture):
        self.fixture = fixture

    def generate_injuries(self):
        '''
        Generate injuries from matchday team selection.
        '''
        if random.randint(0, 100) < 20:
            selection = []

            for player in self.fixture.club.squad.teamselection.team:
                selection.append(player)

                if player.injury.fitness > 100:
                    value = int((100 - player.injury.fitness) % 4)

                    for count in range(0, value):
                        selection.append(player)

            random.shuffle(selection)

            player = random.choice(selection)

            injury = data.injuries.get_random_injury()

            player.injury.injuryid = injury.injuryid
            player.injury.period = random.randint(injury.period[0], injury.period[1])
            player.injury.fitness -= random.randint(injury.impact[0], injury.impact[1])

            if player.club is data.user.club:
                data.user.club.news.publish("IN02",
                                            player=player.get_name(mode=1),
                                            weeks=player.injury.period,
                                            injury=player.injury.get_injury_name())


class Cards:
    def __init__(self, fixture):
        self.fixture = fixture

    def generate_cards(self):
        '''
        Generate yellow and red cards for match.
        '''


class Attendance:
    def __init__(self, fixture):
        self.fixture = fixture

    def get_attendance(self):
        '''
        Return attendance for given fixture.
        '''
        club = self.fixture.home.club

        base = (74000 / (40 - club.reputation)) * club.reputation

        minimum = int(base * -0.1)
        maximum = int(base * 0.1)
        attendance = base + random.randrange(minimum, maximum)

        if attendance > club.stadium.get_capacity():
            attendance = club.stadium.get_capacity()

        return attendance
