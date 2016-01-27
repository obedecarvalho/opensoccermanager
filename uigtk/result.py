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


from gi.repository import Gtk

import data
import uigtk.match
import uigtk.widgets


class Result(uigtk.widgets.Grid):
    '''
    Screen displaying match results, statistics, and data.
    '''
    __name__ = "result"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        grid = uigtk.widgets.Grid()
        grid.set_hexpand(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 0, 0, 1, 1)

        self.labelHome = uigtk.widgets.Label()
        self.labelHome.connect("activate-link", self.on_label_activated)
        grid.attach(self.labelHome, 0, 0, 1, 1)
        self.labelResult = uigtk.widgets.Label()
        grid.attach(self.labelResult, 1, 0, 1, 1)
        self.labelAway = uigtk.widgets.Label()
        self.labelAway.connect("activate-link", self.on_label_activated)
        grid.attach(self.labelAway, 2, 0, 1, 1)

        self.information = uigtk.match.Information()
        grid.attach(self.information, 1, 1, 1, 1)

        self.labelNotPlayed = Gtk.Label("This fixture has not yet been played.")
        self.attach(self.labelNotPlayed, 0, 1, 1, 1)

    def set_visible_result(self, leagueid, fixtureid):
        '''
        Display result information for given fixture id in passed league.
        '''
        league = data.leagues.get_league_by_id(leagueid)
        fixture = league.fixtures.get_fixture_by_id(fixtureid)

        home = data.clubs.get_club_by_id(fixture.home.clubid)
        away = data.clubs.get_club_by_id(fixture.away.clubid)

        self.labelHome.set_markup("<a href='club'><span size='18000'><b>%s</b></span></a>" % (home.name))
        self.labelHome.clubid = fixture.home.clubid
        self.labelAway.set_markup("<a href='club'><span size='18000'><b>%s</b></span></a>" % (away.name))
        self.labelAway.clubid = fixture.away.clubid

        stadium = data.stadiums.get_stadium_by_id(home.stadium)
        self.information.labelStadium.set_label(stadium.name)

        referee = data.referees.get_referee_by_id(fixture.referee)
        self.information.labelReferee.set_label(referee.name)

        self.labelNotPlayed.set_visible(not fixture.played)

        if fixture.played:
            self.labelResult.set_markup("<span size='18000'><b>%i - %i</b></span>" % (fixture.result))

    def on_label_activated(self, label, uri):
        '''
        Activate selected club and display information screen.
        '''
        data.window.screen.change_visible_screen("clubinformation")
        data.window.screen.active.set_visible_club(label.clubid)

        return True

    def run(self):
        self.show_all()
