from identity.account import Account
from identity.alias import Alias
from database.core import db
import pony.orm
import sqlite3


class Database(object):
    """An interface to the in-memory identity database.
    """

    def connect(self):
        db.bind(provider='sqlite', filename=':memory:')
        db.generate_mapping(create_tables=True)

    def __getitem__(self, url):
        """Finds all accounts and corresponding aliases for a given url.

        Args:
            url: The url to which the accounts belong.

        Returns:
            A list of tuples containing an account and its corresponding alias.
        """
        with pony.orm.db_session():
            accounts = pony.orm.select(account for account in db.Account if account.url == url).prefetch(db.Account.alias)[:]
        return accounts

    def _get_accounts(self):
        with pony.orm.db_session():
            accounts = pony.orm.select(account for account in db.Account).prefetch(db.Account.alias)[:]
        return accounts

    def _get_aliases(self):
        with pony.orm.db_session():
            aliases = pony.orm.select(alias for alias in db.Alias).prefetch(db.Alias.accounts)[:]
        return aliases

    @property
    def accounts(self):
        return self._get_accounts()

    @property
    def aliases(self):
        return self._get_aliases()

    def add_alias(self, alias):
        with pony.orm.db_session():
            alias = Alias(**alias)
        return alias

    def add_account(self, account):
        with pony.orm.db_session():
            account = Account(**account)
        return account

    def load(self, dump):
        """Fills the current in-memory sqlite database by executing
        the given dump.

        Args:
            A string containing the database dump data.
        """
        with pony.orm.db_session():
            db.execute(dump)

    def save(self):
        """Dumps the in-memory database and returns the raw data.

        Returns:
            The database dump.
        """
        with pony.orm.db_session():
            connection = db.get_connection()
            dump = "\n".join(connection.iterdump())
        return dump
