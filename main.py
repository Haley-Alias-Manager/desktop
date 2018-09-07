from identity import IdentityHandler
from identity import IdentityGenerator
from database.threaded_database import ThreadedDatabase
from interfaces.firefox import FirefoxComInterface

import sys
from PyQt5.QtWidgets import QApplication, QStyle, QMenu
from PyQt5 import QtGui
from ui import SystemTrayIcon


idg = IdentityGenerator()
db = ThreadedDatabase()
db.start()
idh = IdentityHandler(idg, db)

for i in range(100):
    id1 = idh.create_random_identity("google.com")
id2 = idh.create_random_identity("google.com")
id3 = idh.create_random_identity("google.com")
id4 = idh.create_random_identity("google.com")


def update_account_creation_menu(current_website, account_menu):
    account_menu.clear()
    account_menu.add_title("Alias:")    

    def create_identity():
        idh.create_random_identity(current_website)
        update_account_creation_menu(current_website, account_menu)

    def create_account(alias):
        idh.create_random_account(alias, current_website)

    account_menu.add_action("New Alias", create_identity)
    for alias in db.aliases:
        account_menu.add_action("%s %s" % (alias.first_name, alias.last_name), lambda: create_account(alias))



if __name__ == '__main__':
    app = QApplication(sys.argv)

    style = app.style()
    icon = QtGui.QIcon("icon_small_48.png")
    
    tray_icon = SystemTrayIcon(icon)
    tray_icon.show()

    current_website = "google.com"

    tray_icon.add_action("Generate Alias", lambda: print("hey"))    
    account_menu = tray_icon.add_menu("Generate Account for %s" % current_website)
    tray_icon.add_action("Exit", app.quit)

    update_account_creation_menu(current_website, account_menu)

    ff_interface = FirefoxComInterface(idh)
    ff_interface.start()

    app.exec_()
    ff_interface.stop()
    db.stop()
