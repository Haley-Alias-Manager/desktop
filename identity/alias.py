from database.core import db
from pony.orm import Required, Set
from datetime import date


class Alias(db.Entity):
    _table_        = "aliases"
    email          = Required(str)
    first_name     = Required(str)
    last_name      = Required(str)
    date_of_birth  = Required(date)
    country        = Required(str)
    city           = Required(str)
    accounts       = Set("Account")
