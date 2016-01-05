#!/usr/bin/env python3

from gi.repository import Gtk
from gi.repository import Gdk

import data
import uigtk.aboutdialog
import uigtk.deletedialog
import uigtk.details
import uigtk.filedialog
import uigtk.preferences
import uigtk.widgets


class Welcome(Gtk.Grid):
    '''
    Main menu screen displayed at start of game.
    '''
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(5)
        self.set_row_spacing(5)
        self.set_column_spacing(5)
        self.set_column_homogeneous(True)

        sizegroup = Gtk.SizeGroup()
        sizegroup.set_mode(Gtk.SizeGroupMode.HORIZONTAL)

        label = Gtk.Label()
        sizegroup.add_widget(label)
        self.attach(label, 0, 0, 1, 1)

        buttonbox = Gtk.ButtonBox()
        sizegroup.add_widget(buttonbox)
        buttonbox.set_vexpand(True)
        buttonbox.set_hexpand(True)
        buttonbox.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        buttonbox.set_orientation(Gtk.Orientation.VERTICAL)
        self.attach(buttonbox, 1, 1, 2, 1)

        buttonNew = uigtk.widgets.Button("_New Game")
        buttonNew.set_tooltip_text("Start a new game.")
        buttonNew.connect("clicked", self.on_new_clicked)
        key, modifier = Gtk.accelerator_parse("<Control>N")
        buttonNew.add_accelerator("clicked",
                                  data.window.accelgroup,
                                  key,
                                  modifier,
                                  Gtk.AccelFlags.VISIBLE)
        buttonbox.add(buttonNew)

        buttonLoad = uigtk.widgets.Button("_Load Game")
        buttonLoad.set_tooltip_text("Load a saved game.")
        buttonLoad.connect("clicked", self.on_load_clicked)
        key, modifier = Gtk.accelerator_parse("<Control>L")
        buttonLoad.add_accelerator("clicked",
                                   data.window.accelgroup,
                                   key,
                                   modifier,
                                   Gtk.AccelFlags.VISIBLE)
        buttonbox.add(buttonLoad)

        buttonDelete = uigtk.widgets.Button("_Delete Game")
        buttonDelete.set_tooltip_text("Delete a saved game.")
        buttonDelete.connect("clicked", uigtk.deletedialog.DeleteDialog)
        key, modifier = Gtk.accelerator_parse("<Control>D")
        buttonDelete.add_accelerator("clicked",
                                     data.window.accelgroup,
                                     key,
                                     modifier,
                                     Gtk.AccelFlags.VISIBLE)
        buttonbox.add(buttonDelete)

        buttonPreferences = uigtk.widgets.Button("_Preferences")
        buttonPreferences.set_tooltip_text("Edit the game preferences.")
        buttonPreferences.connect("clicked", uigtk.preferences.Dialog)
        buttonbox.add(buttonPreferences)

        buttonEditor = uigtk.widgets.Button("Data _Editor")
        buttonEditor.set_tooltip_text("Edit the game data.")
        buttonbox.add(buttonEditor)

        buttonQuit = uigtk.widgets.Button("_Quit Game")
        buttonQuit.set_tooltip_text("Quit the game.")
        buttonQuit.connect("clicked", self.on_quit_game)
        key, modifier = Gtk.accelerator_parse("<Control>Q")
        buttonQuit.add_accelerator("activate",
                                   data.window.accelgroup,
                                   key,
                                   modifier,
                                   Gtk.AccelFlags.VISIBLE)
        buttonbox.add(buttonQuit)

        buttonAbout = uigtk.widgets.Button("_Version 0.99 (01011970)")
        buttonAbout.set_relief(Gtk.ReliefStyle.NONE)
        buttonAbout.connect("clicked", uigtk.aboutdialog.AboutDialog)
        self.attach(buttonAbout, 0, 2, 1, 1)

        buttonLink = Gtk.LinkButton("https://opensoccermanager.org/")
        buttonLink.set_label("OpenSoccerManager Website")
        self.attach(buttonLink, 3, 2, 1, 1)

        self.details = uigtk.details.Details()

    def set_show_welcome_screen(self, *args):
        '''
        Remove game interface and restore welcome screen.
        '''
        data.window.mainscreen.grid.remove(data.window.screen)
        data.window.remove(data.window.mainscreen)
        data.window.add(data.window.welcome)

    def on_new_clicked(self, *args):
        '''
        Start new game and load details collection screen.
        '''
        data.window.remove(self)
        data.window.add(self.details)
        self.details.run()

    def on_load_clicked(self, *args):
        '''
        Launch dialog to find previously saved game.
        '''
        uigtk.filedialog.LoadDialog()

    def on_quit_game(self, *args):
        '''
        Request to quit the game.
        '''
        data.window.on_quit_game()
