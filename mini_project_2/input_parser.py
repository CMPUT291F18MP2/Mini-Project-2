""" Class that validates and parses queries """

import re

alphanumeric = r"[0-9a-zA-Z_-]"
numeric = r"[0-9]"
date = r"[0-9]{4}/[0-9]{2}/[0-9]{2}"
date_prefix = r"(date)\s*(>=|<=|=|>|<)"
date_query = date_prefix + r"\s*" + date
price = numeric + r"+"
price_prefix = r"(price)\s*(>=|<=|=|>|<)"
price_query = price_prefix + r"\s*" + price
location = alphanumeric + r"+"
location_prefix = r"(location)\s*="
location_query = location_prefix + r"\s*" + location
cat = alphanumeric + r"+"
cat_prefix = r"(cat)\s*="
cat_query = cat_prefix + r"\s*" + cat
term = alphanumeric + r"+"
term_suffix = r"%"
term_query = term + term_suffix + r"|" + term
expression = r"(" + date_query + r"|" + price_query + r"|" + location_query + r"|" + cat_query + r"|" + term_query + r")"
query = r"\s*" + expression + r"(\s+" + expression + r")*" + r"\s*"

class InputParser():

    def __init__(self):
        self.logger = self.__log_setup()

    def __log_setup(self):
        return None

    def validate_query(self, requested_query):
        """ Validates user input
            Returns true if valid.
            Returns false otherwise
        """
        # Add ^ and $ to the pattern to match the whole string.
        pattern = r"^" + query + r"$"
        if re.match(pattern, requested_query, re.I):
            return True
        else:
            return False

    def parse_input(self, query):
        """ Parses the user input and returns a
            dictionary of the requested searches.
        """
        return None
