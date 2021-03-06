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


class Ability:
    '''
    Ability value for coaches and scouts.
    '''
    def __init__(self):
        self.abilities = {0: "Average",
                          1: "Good",
                          2: "Superb"}

    def get_abilities(self):
        '''
        Return full dictionary of abilities.
        '''
        return self.abilities.items()

    def get_ability_by_id(self, abilityid):
        '''
        Return ability string for given id value.
        '''
        return self.abilities[abilityid]
