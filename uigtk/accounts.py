#!/usr/bin/env python3

from gi.repository import Gtk

import data
import uigtk.widgets


class Accounts(uigtk.widgets.Grid):
    __name__ = "accounts"

    def __init__(self):
        uigtk.widgets.Grid.__init__(self)

        self.income = Income()
        self.attach(self.income, 0, 0, 1, 1)

        self.expenditure = Expenditure()
        self.attach(self.expenditure, 1, 0, 1, 1)

        separator = Gtk.Separator()
        self.attach(separator, 0, 2, 2, 1)

        frame = uigtk.widgets.CommonFrame("Totals")
        self.attach(frame, 0, 3, 1, 1)

        label = uigtk.widgets.Label("Total Income", leftalign=True)
        frame.grid.attach(label, 0, 0, 1, 1)
        self.labelIncome = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelIncome, 1, 0, 1, 1)
        label = uigtk.widgets.Label("Total Expenditure", leftalign=True)
        frame.grid.attach(label, 0, 1, 1, 1)
        self.labelExpenditure = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelExpenditure, 1, 1, 1, 1)
        label = uigtk.widgets.Label("Current Balance", leftalign=True)
        frame.grid.attach(label, 0, 2, 1, 1)
        self.labelBalance = uigtk.widgets.Label(leftalign=True)
        frame.grid.attach(self.labelBalance, 1, 2, 1, 1)

    def run(self):
        club = data.clubs.get_club_by_id(data.user.team)

        self.income.run()
        self.expenditure.run()

        amount = data.currency.get_currency(club.accounts.income, integer=True)
        self.labelIncome.set_label(amount)
        amount = data.currency.get_currency(club.accounts.expenditure, integer=True)
        self.labelExpenditure.set_label(amount)
        amount = data.currency.get_currency(club.accounts.balance, integer=True)
        self.labelBalance.set_label(amount)

        self.show_all()


class Heading(uigtk.widgets.CommonFrame):
    def __init__(self, title=""):
        uigtk.widgets.CommonFrame.__init__(self, title)
        self.set_hexpand(True)
        self.grid.set_column_homogeneous(True)

        label = uigtk.widgets.Label("This Week")
        self.grid.attach(label, 1, 1, 1, 1)
        label = uigtk.widgets.Label("This Season")
        self.grid.attach(label, 2, 1, 1, 1)


class Income(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_hexpand(True)

        self.heading = Heading("Income")
        self.attach(self.heading, 0, 0, 1, 1)

        label = uigtk.widgets.Label("Prize Money", leftalign=True)
        self.heading.grid.attach(label, 0, 2, 1, 1)
        label = uigtk.widgets.Label("Sponsorship", leftalign=True)
        self.heading.grid.attach(label, 0, 3, 1, 1)
        label = uigtk.widgets.Label("Advertising", leftalign=True)
        self.heading.grid.attach(label, 0, 4, 1, 1)
        label = uigtk.widgets.Label("Merchandise", leftalign=True)
        self.heading.grid.attach(label, 0, 5, 1, 1)
        label = uigtk.widgets.Label("Catering", leftalign=True)
        self.heading.grid.attach(label, 0, 6, 1, 1)
        label = uigtk.widgets.Label("Ticket Sales", leftalign=True)
        self.heading.grid.attach(label, 0, 7, 1, 1)
        label = uigtk.widgets.Label("Transfer Fees", leftalign=True)
        self.heading.grid.attach(label, 0, 8, 1, 1)
        label = uigtk.widgets.Label("Loan", leftalign=True)
        self.heading.grid.attach(label, 0, 9, 1, 1)
        label = uigtk.widgets.Label("Grant", leftalign=True)
        self.heading.grid.attach(label, 0, 10, 1, 1)
        label = uigtk.widgets.Label("Television Money", leftalign=True)
        self.heading.grid.attach(label, 0, 11, 1, 1)

        self.labels = []

        for count in range(0, 10):
            label1 = uigtk.widgets.Label(leftalign=True)
            self.heading.grid.attach(label1, 1, count + 2, 1, 1)

            label2 = uigtk.widgets.Label(leftalign=True)
            self.heading.grid.attach(label2, 2, count + 2, 1, 1)

            self.labels.append((label1, label2))

    def run(self):
        club = data.clubs.get_club_by_id(data.user.team)

        for count, (key, item) in enumerate(club.accounts.incomes.items()):
            amount = data.currency.get_currency(item.week, integer=True)
            self.labels[count][0].set_label("%s" % (amount))

            amount = data.currency.get_currency(item.season, integer=True)
            self.labels[count][1].set_label("%s" % (amount))


class Expenditure(uigtk.widgets.Grid):
    def __init__(self):
        uigtk.widgets.Grid.__init__(self)
        self.set_hexpand(True)

        self.heading = Heading("Expenditure")
        self.attach(self.heading, 0, 0, 1, 1)

        label = uigtk.widgets.Label("Fines", leftalign=True)
        self.heading.grid.attach(label, 0, 2, 1, 1)
        label = uigtk.widgets.Label("Stadium", leftalign=True)
        self.heading.grid.attach(label, 0, 3, 1, 1)
        label = uigtk.widgets.Label("Staff Wages", leftalign=True)
        self.heading.grid.attach(label, 0, 4, 1, 1)
        label = uigtk.widgets.Label("Player Wages", leftalign=True)
        self.heading.grid.attach(label, 0, 5, 1, 1)
        label = uigtk.widgets.Label("Transfer Fees", leftalign=True)
        self.heading.grid.attach(label, 0, 6, 1, 1)
        label = uigtk.widgets.Label("Merchandise", leftalign=True)
        self.heading.grid.attach(label, 0, 7, 1, 1)
        label = uigtk.widgets.Label("Catering", leftalign=True)
        self.heading.grid.attach(label, 0, 8, 1, 1)
        label = uigtk.widgets.Label("Loan Repayment", leftalign=True)
        self.heading.grid.attach(label, 0, 9, 1, 1)
        label = uigtk.widgets.Label("Overdraft Repayment", leftalign=True)
        self.heading.grid.attach(label, 0, 10, 1, 1)
        label = uigtk.widgets.Label("Training", leftalign=True)
        self.heading.grid.attach(label, 0, 11, 1, 1)

        self.labels = []

        for count in range(0, 10):
            label1 = uigtk.widgets.Label(leftalign=True)
            self.heading.grid.attach(label1, 1, count + 2, 1, 1)

            label2 = uigtk.widgets.Label(leftalign=True)
            self.heading.grid.attach(label2, 2, count + 2, 1, 1)

            self.labels.append((label1, label2))

    def run(self):
        club = data.clubs.get_club_by_id(data.user.team)

        for count, (key, item) in enumerate(club.accounts.expenditures.items()):
            amount = data.currency.get_currency(item.week, integer=True)
            self.labels[count][0].set_label("%s" % (amount))

            amount = data.currency.get_currency(item.season, integer=True)
            self.labels[count][1].set_label("%s" % (amount))


class NotEnoughFunds(Gtk.MessageDialog):
    '''
    Display dialog when there is not enough money to complete the transaction.
    '''
    def __init__(self):
        Gtk.MessageDialog.__init__(self)
        self.set_transient_for(data.window)
        self.set_title("Not Enough Funds")
        self.set_property("message-type", Gtk.MessageType.ERROR)
        self.set_markup("There are not enough funds to complete this transaction.")
        self.add_button("_Close", Gtk.ResponseType.CLOSE)
        self.connect("response", self.on_response)

        self.show()

    def on_response(self, *args):
        self.destroy()
