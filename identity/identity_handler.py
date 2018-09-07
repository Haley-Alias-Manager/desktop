

class IdentityHandler(object):
    """Holds convenience functions to access and create aliases
    and accounts.

    Args:
        identity_generator: An instance of an IdentityGenerator object.
        database: An instance of a database object.
    """

    def __init__(self, identity_generator, database):
        self.identity_generator = identity_generator
        self.identities = database

    def create_random_identity(self, url):
        """Creates a random alias and associated account for a given url.

        Args:
            url: The url of the website for which to create the account.

        Returns:
            A tuple containing the new alias and account.
        """
        alias = self.create_random_alias()
        account = self.create_random_account(alias, url)
        return alias, account

    def create_random_alias(self):
        """Creates a random alias.

        Returns:
            The new alias.
        """
        alias_info = self.identity_generator.generate_alias()
        alias = self.identities.add_alias(alias_info)
        self.identities.save()
        return alias

    def create_random_account(self, alias, url):
        """Creates a random account.

        Args:
            alias: The alias to which to associate the account.
            url: The url of the website for which to create the account.

        Returns:
            The new account.
        """
        account_info = self.identity_generator.generate_account(alias, url)
        account = self.identities.add_account(account_info)
        self.identities.save()
        return account
