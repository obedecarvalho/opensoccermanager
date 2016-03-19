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


class TeamTraining:
    def __init__(self):
        self.team_training = [0] * 42

        self.timeout = 6

    def get_training(self):
        '''
        Get list of team training index values.
        '''
        return self.team_training

    def set_training(self, index, value):
        '''
        Set team training value for given index in list.
        '''
        self.team_training[index] = value

        self.get_random_timeout()

    def get_random_schedule(self):
        '''
        Apply new random schedule for team training.
        '''
        values = [count for count in range(2, 18)]
        random.shuffle(values)

        for count in range(0, 6):
            self.team_training[count * 6] = values[count * 2]
            self.team_training[count * 6 + 1] = values[count * 2 + 1]
            self.team_training[count * 6 + 2] = 1
            self.team_training[count * 6 + 3] = 0
            self.team_training[count * 6 + 4] = 0
            self.team_training[count * 6 + 5] = 0

        self.get_random_timeout()

    def get_random_timeout(self):
        '''
        Get random number of weeks for timeout.
        '''
        self.timeout = random.randint(8, 12)

    def get_sunday_training(self):
        '''
        Return True if team is training on Sunday.
        '''
        sunday = False

        for trainingid in self.team_training[36:42]:
            if trainingid != 0:
                sunday = True
                break

        return sunday

    def get_overworked_training(self):
        '''
        Return True if the team is being overworked.
        '''
        count = sum(1 for trainingid in self.team_training if trainingid != 0)
        overworked = count > 18

        return overworked

    def get_schedule_set(self):
        '''
        Return whether a schedule has been set.
        '''
        return self.team_training != [0] * 42

    def get_individual_set(self):
        '''
        Return whether individual training has been assigned.
        '''
        return 1 in self.team_training

    def get_individual_sessions(self):
        '''
        Return number of individual sessions set in training schedule.
        '''
        return sum(1 for item in self.team_training if item == 1)

    def update_schedule(self):
        '''
        Generate new training schedule and apply.
        '''
        if self.timeout > 0:
            self.timeout -= 1

            if self.timeout == 0:
                if self.get_schedule_set():
                    data.user.club.news.publish("TT02")
                    self.get_random_timeout()
                else:
                    data.user.club.news.publish("TT01")
                    self.get_random_timeout()

                if self.get_sunday_training():
                    data.user.club.news.publish("TT03")

                if self.get_overworked_training():
                    data.user.club.news.publish("TT04")
