from database.core import db
from pony.orm import Required


class Account(db.Entity):
    _table_  = "accounts"
    url      = Required(str)
    username = Required(str)
    password = Required(str)
    email    = Required(str)
    alias    = Required("Alias")
