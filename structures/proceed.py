#!/usr/bin/env python3

import data
import structures.advertising
import uigtk.match


class ContinueGame:
    '''
    Class handling proceeding with the game to the next event.
    '''
    def __init__(self):
        self.continuetomatch = ContinueToMatch()
        self.continue_allowed = 0

    def on_continue_game(self):
        '''
        Determine whether game will continue, or handle if there is a match.
        '''
        if self.continue_allowed == 0:
            if not data.calendar.get_fixture():
                data.date.increment_date()
                data.window.screen.refresh_visible_screen()

            if data.calendar.get_fixture():
                data.calendar.get_user_fixture()
                self.continue_allowed = 1

        if self.continue_allowed == 1:
            self.continue_allowed = 2
        elif self.continue_allowed == 2:
            opposition = data.calendar.get_user_opposition()

            if self.on_continue_to_match(opposition):
                self.continue_allowed = 3
        elif self.continue_allowed == 3:
            data.window.screen.change_visible_screen("squad")
            data.calendar.increment_event()
            self.continue_allowed = 0

    def on_continue_to_match(self, clubid):
        '''
        Determine whether match can continue or display error.
        '''
        if self.continuetomatch.get_valid_squad():
            club = data.clubs.get_club_by_id(clubid)
            dialog = uigtk.match.ProceedToMatch(club.name)

            if dialog.show():
                if self.continuetomatch.get_selected_substitutes():
                    return True
                else:
                    return False
        else:
            return False


class ContinueToMatch:
    '''
    Class to verify whether next match is able to be played.
    '''
    def get_valid_squad(self):
        '''
        Verify eleven selected players are eligible.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        count = club.squad.teamselection.get_team_count()

        state = count == 11

        if not state:
            uigtk.match.NotEnoughPlayers(count)

        return state

    def get_selected_substitutes(self):
        '''
        Check whether the user has selected all substitutes.
        '''
        club = data.clubs.get_club_by_id(data.user.team)
        count = club.squad.teamselection.get_subs_count()

        state = True

        if count < 5:
            dialog = uigtk.match.NotEnoughSubs(count)
            state = dialog.show()

        if state:
            fixtureid, fixture = data.calendar.get_user_fixture()

            data.window.screen.change_visible_screen("match")
            data.window.screen.active.update_match_details(fixtureid, fixture)

        return state