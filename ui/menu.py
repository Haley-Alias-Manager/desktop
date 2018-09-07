from PyQt5.QtWidgets import QMenu


class Menu(QMenu):

    def __init__(self, name="", parent=None):
        QMenu.__init__(self, name, parent)

    def add_title(self, title):
        action = self.add_action(title, lambda: None)
        action.setDisabled(True)
        return action

    def add_action(self, name, function):
        action = self.addAction(name)
        action.triggered.connect(function)
        return action

    def add_menu(self, menu):
        self.addMenu(menu)
