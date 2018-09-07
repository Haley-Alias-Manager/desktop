from identity.alias import Alias
from identity.account import Account

import os
import uuid
import math
import base64
import random
import datetime


class IdentityGenerator(object):
    """Generates random aliases and accounts using predefined rules.
    """

    def __init__(self, min_pass_length=14):
        self.min_pass_length = min_pass_length

    def _generate_password(self, min_length):
        # b64 encoding length calculation
        num_bytes = math.ceil(3 * min_length / 4)
        rand = os.urandom(num_bytes)
        password = base64.b64encode(rand).decode("utf8")
        return password

    def _generate_username(self, alias=None):
        return str(uuid.uuid4())

    def _generate_email(self, first_name, last_name, provider="gmail.com"):
        """Generates a new email for a given alias.

        Args:
            alias: The alias to which the email belongs.
            provider: The email provider. Default: gmail.com

        Returns:
            A new email address that will have to be registered.
        """
        number = random.randint(1000, 9999)
        return "%s.%s.%s@%s" % (first_name, last_name, number, provider)

    def _generate_date_of_birth(self):
        year  = random.randint(1950, 2000)
        month = random.randint(1, 12)
        day   = random.randint(1, 28)
        date_of_birth = datetime.date(year, month, day)
        return date_of_birth

    def _generate_country(self):
        return "United-Kingdom"

    def _generate_city(self, country):
        return "London"

    def generate_alias(self):
        """Generates a new random alias.

        Returns:
            A dictionary containing the alias' info.
        """
        country       = self._generate_country()
        first_name    = self._generate_username()
        last_name     = self._generate_username()
        email         = self._generate_email(first_name, last_name)
        date_of_birth = self._generate_date_of_birth()
        city          = self._generate_city(country)
        alias = {
            "email":         email,
            "first_name":    first_name,
            "last_name":     last_name,
            "date_of_birth": date_of_birth,
            "country":       country,
            "city":          city
        }
        return alias

    def generate_account(self, alias, url, email=None):
        """Generates a new random account.

        Args:
            alias: The alias to associate the account with.
            url: The url of the website where the account is used.
            email: The email to use for registration, if None an old one
                from this alias is used or a new one generated.
                Default: None

        Returns:
            The new account.
        """
        username = self._generate_username()
        password = self._generate_password(self.min_pass_length)
        email    = alias.email

        account = {
            "url":      url,
            "username": username,
            "password": password,
            "email":    email,
            "alias":    alias.id
        }
        return account
