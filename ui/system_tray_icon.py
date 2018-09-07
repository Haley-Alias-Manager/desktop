from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from ui.menu import Menu


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = Menu(parent)
        self.setContextMenu(self.menu)

    def add_action(self, name, function):
        action = self.menu.add_action(name, function)
        return action

    def add_menu(self, name):
        menu = Menu(name, self.menu)
        self.menu.add_menu(menu)
        return menu
