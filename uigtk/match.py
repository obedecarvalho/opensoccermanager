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
import uigtk.widgets


class Match(uigtk.widgets.Grid):
    '''
    Interface handling display of match related widgets.
    '''
    __name__ = "match"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        buttonbox = uigtk.widgets.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.START)
        self.attach(buttonbox, 0, 0, 1, 1)

        self.buttonStart = uigtk.widgets.Button("_Start Match")
        self.buttonStart.connect("clicked", self.on_start_match_clicked)
        buttonbox.add(self.buttonStart)

        self.buttonHomeTactics = uigtk.widgets.Button()
        buttonbox.add(self.buttonHomeTactics)
        self.buttonAwayTactics = uigtk.widgets.Button()
        buttonbox.add(self.buttonAwayTactics)

        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_column_homogeneous(True)
        self.attach(grid, 1, 0, 1, 1)

        self.score = Score()
        grid.attach(self.score, 0, 0, 1, 1)

        self.information = Information()
        self.score.attach(self.information, 1, 1, 1, 1)

    def update_match_details(self, fixtureid, fixture):
        '''
        Set match details for given fixture.
        '''
        self.score.set_teams(fixtureid, fixture)
        self.set_tactics_buttons(fixtureid, fixture)

        club = data.clubs.get_club_by_id(fixture.home)
        stadium = data.stadiums.get_stadium_by_id(club.stadium)
        self.information.set_information(stadium.name, "Test")

    def set_tactics_buttons(self, fixtureid, fixture):
        '''
        Update label on tactics buttons to display club names.
        '''
        self.buttonHomeTactics.set_label("_%s\nTactics" % (fixture.get_home_name()))
        self.buttonAwayTactics.set_label("_%s\nTactics" % (fixture.get_away_name()))

    def on_start_match_clicked(self, button):
        '''
        Call match engine to generate result, then enable interface elements.
        '''
        print("Generate result here...")
        button.set_sensitive(False)

        data.window.mainscreen.menu.set_sensitive(True)
        data.window.mainscreen.information.set_continue_game_button()
        data.window.mainscreen.information.buttonContinue.set_sensitive(True)
        data.window.mainscreen.information.buttonNews.set_sensitive(True)

    def run(self):
        data.window.mainscreen.menu.set_sensitive(False)
        data.window.mainscreen.information.buttonContinue.set_sensitive(False)
        data.window.mainscreen.information.buttonNews.set_sensitive(False)
        data.window.mainscreen.information.buttonNextMatch.set_label("")
        data.window.mainscreen.information.buttonNextMatch.set_visible(False)

        self.buttonStart.set_sensitive(True)

        self.show_all()


class Score(Gtk.Grid):
    '''
    Class to display and update both teams and scores.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_hexpand(True)
        self.set_column_homogeneous(True)

        self.labelHomeTeam = uigtk.widgets.Label()
        self.labelHomeTeam.set_hexpand(True)
        self.attach(self.labelHomeTeam, 0, 0, 1, 1)

        self.labelScore = uigtk.widgets.Label()
        self.labelScore.set_hexpand(True)
        self.attach(self.labelScore, 1, 0, 1, 1)

        self.labelAwayTeam = uigtk.widgets.Label()
        self.labelAwayTeam.set_hexpand(True)
        self.attach(self.labelAwayTeam, 2, 0, 1, 1)

    def set_teams(self, fixtureid, fixture):
        '''
        Set competing team names and 0-0 scoreline.
        '''
        self.labelHomeTeam.set_markup("<span size='24000'><b>%s</b></span>" % (fixture.get_home_name()))
        self.labelAwayTeam.set_markup("<span size='24000'><b>%s</b></span>" % (fixture.get_away_name()))
        self.set_score((0, 0))

    def set_score(self, score):
        '''
        Set current score on label.
        '''
        self.labelScore.set_markup("<span size='24000'><b>%i - %i</b></span>" % (score))


class Information(uigtk.widgets.Grid):
    '''
    Information display of match venue and chosen referee.
    '''
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        label = uigtk.widgets.Label("Stadium", leftalign=True)
        self.attach(label, 0, 0, 1, 1)

        self.labelStadium = uigtk.widgets.Label(leftalign=True)
        self.labelStadium.set_hexpand(True)
        self.attach(self.labelStadium, 1, 0, 1, 1)

        label = uigtk.widgets.Label("Referee", leftalign=True)
        self.attach(label, 0, 1, 1, 1)

        self.labelReferee = uigtk.widgets.Label(leftalign=True)
        self.labelReferee.set_hexpand(True)
        self.attach(self.labelReferee, 1, 1, 1, 1)

    def set_information(self, stadium, referee):
        '''
        Update stadium and referee information.
        '''
        self.labelStadium.set_label(stadium)
        self.labelReferee.set_label(referee)


class ProceedToMatch(Gtk.MessageDialog):
    '''
    Message dialog asking to confirm continuance to next match.
    '''
    def __init__(self, opposition):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Proceed To Match")
        self.set_markup("Proceed to match against %s?" % (opposition))
        self.set_property("message-type", Gtk.MessageType.QUESTION)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state


class NotEnoughPlayers(Gtk.MessageDialog):
    '''
    Error dialog displayed when there aren't enough selected players.
    '''
    def __init__(self, count):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Not Enough Players")

        if count == 0:
            message = "No players have been selected for this match."
        else:
            message = "You have selected only %i of the required 11 players." % (count)

        self.set_markup(message)
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.add_button("_Close", Gtk.ResponseType.CANCEL)
        self.set_default_response(Gtk.ResponseType.CANCEL)
        self.connect("response", self.on_response)

        self.run()

    def on_response(self, *args):
        self.destroy()


class NotEnoughSubs(Gtk.MessageDialog):
    '''
    Confirmation dialog on whether to proceed with less than five substitutes.
    '''
    def __init__(self, count):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_modal(True)
        self.set_title("Not Enough Substitutes")

        if count == 0:
            message = "No substitutes have been selected for this match."
        else:
            message = "You have selected only %i of 5 substitutes." % (count)

        self.set_markup("<span size='12000'><b>%s</b></span>" % (message))
        self.format_secondary_text("Do you wish to proceed to the game anyway?")
        self.set_property("message-type", Gtk.MessageType.WARNING)
        self.add_button("_Do Not Proceed", Gtk.ResponseType.CANCEL)
        self.add_button("_Proceed", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

    def show(self):
        state = self.run() == Gtk.ResponseType.OK
        self.destroy()

        return state
