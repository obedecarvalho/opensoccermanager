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
from gi.repository import GdkPixbuf
import gi
import glob
import os
import platform

import game
import music
import preferences
import user
import version
import widgets


class OpenDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Open File")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Open", Gtk.ResponseType.OK)
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.set_current_folder(game.save_location)
        self.connect("response", self.response_handler)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Saved Game")
        filefilter.add_pattern("*.osm")
        self.add_filter(filefilter)

    def display(self):
        state = False

        if self.run() == Gtk.ResponseType.OK:
            state = True

        self.destroy()

        return state

    def response_handler(self, filechooserdialog, response):
        if response == Gtk.ResponseType.OK:
            filename = self.get_filename()
            fileio.open_file(filename)


class SaveDialog(Gtk.FileChooserDialog):
    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Save File")
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Save", Gtk.ResponseType.OK)
        self.connect("response", self.response_handler)

        filefilter = Gtk.FileFilter()
        filefilter.set_name("Saved Game")
        filefilter.add_pattern("*.osm")
        self.add_filter(filefilter)

    def display(self):
        self.set_current_folder(game.save_location)
        self.show_all()

        state = True

        if self.run() == Gtk.ResponseType.OK:
            state = False

        return state

    def response_handler(self, filechooserdialog, response):
        if response == Gtk.ResponseType.OK:
            if self.confirm_overwrite() == Gtk.FileChooserConfirmation.ACCEPT_FILENAME:
                self.hide()
        else:
            self.hide()

    def confirm_overwrite(self):
        folder, filename = self.file_extension()

        items = folder.split(os.sep)
        count = len(items) - 1
        foldername = items[count]

        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            fileio.save_file(filepath)
            return Gtk.FileChooserConfirmation.ACCEPT_FILENAME

        dialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION)
        dialog.set_transient_for(game.window)
        dialog.set_markup("<span size='12000'><b>A file named '%s' already exists. Do you want to replace it?</b></span>" % (filename))
        dialog.format_secondary_text("The file already exists in '%s'. Replacing it will overwrite its content." % (foldername))
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Replace", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            fileio.save_file(filepath)
            return Gtk.FileChooserConfirmation.ACCEPT_FILENAME
        else:
            return Gtk.FileChooserConfirmation.SELECT_AGAIN

    def file_extension(self):
        folder = self.get_current_folder()
        filename = self.get_current_name()

        if not filename.endswith(".osm"):
            filename = "%s.osm" % (filename)

        return folder, filename


class DeleteDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_default_size(225, 350)
        self.set_border_width(5)
        self.set_title("Delete File")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.vbox.set_spacing(5)

        filechooser = Gtk.FileChooserButton()
        filechooser.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        filechooser.set_current_folder(game.save_location)
        filechooser.connect("file-set", self.load_directory)
        self.vbox.add(filechooser)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                  Gtk.PolicyType.AUTOMATIC)
        self.vbox.add(scrolledwindow)

        self.liststore = Gtk.ListStore(str, str)
        treemodelsort = Gtk.TreeModelSort(self.liststore)
        treemodelsort.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self.load_directory(location=game.save_location)

        treeview = Gtk.TreeView()
        treeview.set_vexpand(True)
        treeview.set_model(treemodelsort)
        treeview.set_search_column(1)
        treeview.set_headers_visible(False)
        treeview.set_rubber_banding(True)
        self.treeselection = treeview.get_selection()
        self.treeselection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.treeselection.connect("changed", self.selection_changed)
        scrolledwindow.add(treeview)

        cellrenderertext = Gtk.CellRendererText()
        treeviewcolumn = Gtk.TreeViewColumn(None,
                                            cellrenderertext,
                                            text=1)
        treeview.append_column(treeviewcolumn)

        buttonbox = Gtk.ButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.END)
        self.buttonDelete = widgets.Button("_Delete")
        self.buttonDelete.set_sensitive(False)
        self.buttonDelete.connect("clicked", self.delete_file)
        buttonbox.add(self.buttonDelete)
        self.vbox.add(buttonbox)

    def load_directory(self, filechooser=None, location=None):
        self.liststore.clear()

        if filechooser:
            location = filechooser.get_uri()
            location = location[7:]

        filenames = glob.glob("%s/*.osm" % (location))

        for filepath in filenames:
            filename = os.path.split(filepath)
            self.liststore.append([filepath, filename[1]])

    def selection_changed(self, treeselection):
        model, treepath = treeselection.get_selected_rows()
        self.buttonDelete.set_sensitive(treepath)

    def delete_file(self, button):
        model, treepath = self.treeselection.get_selected_rows()

        for item in treepath:
            filepath = model[item][0]
            os.remove(filepath)

        self.load_directory(location=game.save_location)

    def display(self):
        self.show_all()
        self.run()
        self.destroy()


class AboutDialog(Gtk.AboutDialog):
    def __init__(self):
        path = os.path.join("resources", "logo.svg")
        icon = GdkPixbuf.Pixbuf.new_from_file_at_size(path, 64, 64)

        Gtk.AboutDialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_program_name("%s" % (version.NAME))
        self.set_version("%s" % (version.VERSION))
        self.set_comments("%s" % (version.COMMENTS))
        self.set_website("%s" % (version.WEBSITE))
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_authors([version.AUTHORS])
        self.set_logo(icon)

    def display(self):
        self.run()
        self.destroy()


class HelpDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("Help Contents")
        self.set_transient_for(game.window)
        self.set_default_size(480, 320)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_hexpand(True)
        self.vbox.add(scrolledwindow)

        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.set_left_margin(5)
        textview.set_right_margin(5)
        scrolledwindow.add(textview)
        self.textbuffer = textview.get_buffer()

    def display(self):
        name = game.active_screen.__name__
        filename = os.path.join("help", "%s.txt" % (name))

        try:
            fp = open(filename, "r")
            content = fp.read()
            content = content.rstrip("\n")
            fp.close()
        except FileNotFoundError:
            return

        self.textbuffer.set_text(content, -1)

        self.show_all()
        self.run()
        self.destroy()


class InfoDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_transient_for(game.window)
        self.set_title("Information")
        self.set_border_width(5)
        self.add_button("_Close", Gtk.ResponseType.CLOSE)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.AlignedLabel("Python version")
        grid.attach(label, 0, 0, 1, 1)
        label = widgets.AlignedLabel("%s" % (platform.python_version()))
        grid.attach(label, 1, 0, 1, 1)

        label = widgets.AlignedLabel("GTK+ version")
        grid.attach(label, 0, 1, 1, 1)
        label = widgets.AlignedLabel("%i.%i.%i" % (Gtk.MAJOR_VERSION,
                                                   Gtk.MINOR_VERSION,
                                                   Gtk.MICRO_VERSION))
        grid.attach(label, 1, 1, 1, 1)

        label = widgets.AlignedLabel("GObject version")
        grid.attach(label, 0, 2, 1, 1)
        label = widgets.AlignedLabel("%i.%i.%i" % (gi.version_info))
        grid.attach(label, 1, 2, 1, 1)

    def display(self):
        self.show_all()
        self.run()
        self.destroy()


class NameChange(Gtk.Dialog):
    def __init__(self):
        self.state = False

        Gtk.Dialog.__init__(self)
        self.set_title("Manager Name")
        self.set_transient_for(game.window)
        self.set_border_width(5)
        self.set_resizable(False)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Apply", Gtk.ResponseType.APPLY)
        self.set_default_response(Gtk.ResponseType.APPLY)
        self.connect("response", self.response_handler)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        label = widgets.Label("Change Your Manager _Name:")
        grid.attach(label, 0, 0, 1, 1)

        self.liststoreName = Gtk.ListStore(str)

        combobox = Gtk.ComboBoxText.new_with_entry()
        combobox.set_model(self.liststoreName)
        self.entry = combobox.get_child()
        label.set_mnemonic_widget(combobox)
        grid.attach(combobox, 1, 0, 1, 1)

        self.user = user.Names()

    def display(self):
        self.load_names()

        club = user.get_user_club()
        self.entry.set_text(club.manager)

        self.show_all()
        self.run()

        return self.state

    def response_handler(self, dialog, response):
        if response == Gtk.ResponseType.APPLY:
            club = user.get_user_club()
            club.manager = self.entry.get_text()

            self.user.add_name(club.manager)

            self.load_names()

            self.state = True

        self.destroy()

    def load_names(self):
        '''
        Load list of names to display in dropdown.
        '''
        self.liststoreName.clear()

        for name in self.user.read_names():
            self.liststoreName.append([name])


class PreferencesDialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)
        self.set_title("Preferences")
        self.set_transient_for(game.window)
        self.set_resizable(False)
        self.add_button("_Close", Gtk.ResponseType.OK)
        self.set_border_width(5)
        self.vbox.set_spacing(5)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        self.vbox.add(grid)

        checkbuttonMusic = Gtk.CheckButton("Play (annoying) USM Music in Background")
        checkbuttonMusic.set_active(music.music.playing)
        checkbuttonMusic.connect("toggled", self.music_handler)
        grid.attach(checkbuttonMusic, 0, 0, 3, 1)

        label = widgets.AlignedLabel("In-Game Starting Screen")
        grid.attach(label, 0, 1, 1, 1)
        comboboxScreen = Gtk.ComboBoxText()
        comboboxScreen.append("1", "Squad")
        comboboxScreen.append("2", "Fixtures")
        comboboxScreen.append("3", "News")
        comboboxScreen.append("20", "Player Search")
        comboboxScreen.set_active_id(str(preferences.preferences.start_screen))
        comboboxScreen.set_tooltip_text("Choose which screen should first appear when starting new and loading saved games.")
        comboboxScreen.connect("changed", self.change_screen)
        grid.attach(comboboxScreen, 1, 1, 3, 1)

        label = widgets.AlignedLabel("Display Currency")
        grid.attach(label, 0, 2, 1, 1)
        comboboxCurrency = Gtk.ComboBoxText()
        comboboxCurrency.append("0", "British Pound")
        comboboxCurrency.append("1", "U.S. Dollar")
        comboboxCurrency.append("2", "Euro")
        comboboxCurrency.set_active_id(str(preferences.preferences.currency))
        comboboxCurrency.set_tooltip_text("The monetary currency which will be used during the game.")
        comboboxCurrency.connect("changed", self.change_currency)
        grid.attach(comboboxCurrency, 1, 2, 3, 1)

        # Data locations
        frame = widgets.CommonFrame("Data Locations")
        self.vbox.add(frame)

        grid1 = Gtk.Grid()
        grid1.set_row_spacing(5)
        grid1.set_column_spacing(5)
        frame.insert(grid1)

        label = widgets.AlignedLabel("Default Database Location")
        grid1.attach(label, 0, 0, 1, 1)
        filechooserDatabaseLocation = Gtk.FileChooserButton()
        filechooserDatabaseLocation.set_tooltip_text("Location of default database file to load.")
        filechooserDatabaseLocation.set_action(Gtk.FileChooserAction.OPEN)
        filechooserDatabaseLocation.set_filename(os.path.join("databases", game.database_filename))
        filechooserDatabaseLocation.connect("file-set", self.change_database_default)
        grid1.attach(filechooserDatabaseLocation, 1, 0, 1, 1)

        label = widgets.AlignedLabel("Data File Location")
        grid1.attach(label, 0, 1, 1, 1)
        filechooserSaveLocation = Gtk.FileChooserButton()
        filechooserSaveLocation.set_tooltip_text("Default location where game data is stored.")
        filechooserSaveLocation.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        filechooserSaveLocation.set_filename(game.data_location)
        filechooserSaveLocation.connect("file-set", self.change_data_location)
        grid1.attach(filechooserSaveLocation, 1, 1, 1, 1)

        # Manager names
        frame = widgets.CommonFrame("Manager Names")
        self.vbox.add(frame)

        grid1 = Gtk.Grid()
        grid1.set_column_spacing(5)
        frame.insert(grid1)

        label = widgets.AlignedLabel("Clear previously entered manager names:")
        grid1.attach(label, 0, 0, 1, 1)
        buttonbox = Gtk.ButtonBox()
        grid1.attach(buttonbox, 1, 0, 1, 1)
        buttonClear = widgets.Button("_Clear Names")
        buttonClear.connect("clicked", self.clear_names)
        buttonbox.add(buttonClear)

    def music_handler(self, checkbutton):
        if not music.music.playing:
            music.music.play()
            music.music.playing = True
            preferences.preferences["AUDIO"]["PlayMusic"] = "True"
        else:
            music.music.stop()
            music.music.playing = False
            preferences.preferences["AUDIO"]["PlayMusic"] = "False"

        preferences.preferences.writefile()

    def change_currency(self, combobox):
        preferences.preferences["INTERFACE"]["Currency"] = combobox.get_active_id()
        preferences.preferences.writefile()

        preferences.preferences.currency = int(preferences.preferences.currency)

    def change_screen(self, combobox):
        preferences.preferences["INTERFACE"]["StartScreen"] = combobox.get_active_id()
        preferences.preferences.writefile()

    def change_database_default(self, filechooser):
        directory = filechooser.get_uri()
        game.database_filename = directory[7:]

        preferences.preferences["DATABASE"]["Database"] = game.database_filename
        preferences.preferences.writefile()

    def change_data_location(self, filechooser):
        directory = filechooser.get_uri()
        game.data_location = directory[7:]

        preferences.preferences["SAVE"]["Data"] = game.data_location
        preferences.preferences["SAVE"]["Saves"] = os.path.join(game.data_location, "saves")
        preferences.preferences.writefile()

    def clear_names(self, button):
        filepath = os.path.join(game.data_location, "users.txt")
        open(filepath, "w")

    def display(self):
        self.show_all()
        self.run()
        self.destroy()


class ExitDialog(Gtk.MessageDialog):
    def __init__(self):
        Gtk.MessageDialog.__init__(self, type=Gtk.MessageType.QUESTION)
        self.set_transient_for(game.window)
        self.set_title("Exit Game")
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("_Do Not Save", Gtk.ResponseType.REJECT)
        self.add_button("_Save", Gtk.ResponseType.ACCEPT)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.set_markup("<span size='12000'><b>The game has not been saved.</b></span>")

    def display(self, leave=False):
        if leave:
            message = "Do you want to save before starting a new game?"
        else:
            message = "Do you want to save before closing?"

        self.format_secondary_text(message)

        response = self.run()

        state = True

        if response == Gtk.ResponseType.REJECT:
            state = False
        elif response == Gtk.ResponseType.ACCEPT:
            save_dialog = SaveDialog()
            state = save_dialog.display()
            save_dialog.destroy()

        self.destroy()

        return state