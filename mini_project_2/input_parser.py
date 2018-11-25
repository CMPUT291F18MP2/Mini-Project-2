""" Class that validates and parses queries """

import re

alphanumeric = r"[0-9a-zA-Z_-]"
numeric = r"[0-9]"
date = r"([0-9]{4}/[0-9]{2}/[0-9]{2})"
date_prefix = r"(date)\s*(>=|<=|=|>|<)"
date_query = date_prefix + r"\s*" + date
price = r"(" + numeric + r"+)"
price_prefix = r"(price)\s*(>=|<=|=|>|<)"
price_query = price_prefix + r"\s*" + price
location = r"(" + alphanumeric + r"+)"
location_prefix = r"(location)\s*(=)"
location_query = location_prefix + r"\s*" + location
cat = r"(" + alphanumeric + r"+)"
cat_prefix = r"(cat)\s*(=)"
cat_query = cat_prefix + r"\s*" + cat
term = r"(" + alphanumeric + r"+)"
term_suffix = r"(%)"
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

    def parse_input(self, requested_query):
        """ Parses the user input and returns a
            dictionary of the requested searches.
        """
        search_dict = dict()
        requested_query = self.parse_for_date(requested_query, search_dict)
        requested_query = self.parse_for_price(requested_query, search_dict)
        requested_query = self.parse_for_location(requested_query, search_dict)
        requested_query = self.parse_for_category(requested_query, search_dict)
        requested_query = self.parse_for_keyword(requested_query, search_dict)
        return search_dict

    def parse_for_date(self, input_query, search_dict):
        """ Parses input_query for a date search.
            Adds any date searches to search_dict.
            Returns the input_query with dates removed.
        """
        operator_value_pairs = list()
        date_search_patterns = re.findall(date_query, input_query, re.I)

        # date_search_pattern = a list of ("date", operator, value)
        for item in date_search_patterns:
            operator_value_pairs.append((item[1], item[2]))

        if 'date' in search_dict:
            for item in operator_value_pairs:
                search_dict['date'].append(item)
        elif operator_value_pairs:
            search_dict['date'] = operator_value_pairs

        input_query = re.sub(date_query, '', input_query, flags=re.I)
        return input_query

    def parse_for_price(self, input_query, search_dict):
        """ Parses input_query for a price search.
            Adds any price searches to search_dict.
            Returns the input_query with prices removed.
        """
        operator_value_pairs = list()
        price_search_patterns = re.findall(price_query, input_query, re.I)

        # price_search_patterns = a list of ("price", operator, value)
        for item in price_search_patterns:
            operator_value_pairs.append((item[1], item[2]))

        if 'price' in search_dict:
            for item in operator_value_pairs:
                search_dict['price'].append(item)
        elif operator_value_pairs:
            search_dict['price'] = operator_value_pairs

        # remove prices from the query and return it
        input_query = re.sub(price_query, '', input_query, flags=re.I)
        return input_query

    def parse_for_location(self, input_query, search_dict):
        """ Parses input_query for a location search.
            Adds any location searches to search_dict.
            Returns the input_query with locations removed.
        """
        operator_value_pairs = list()
        location_search_patterns = re.findall(location_query, input_query, re.I)

        # location_search_patterns = a list of ("location", "=", value)
        for item in location_search_patterns:
            operator_value_pairs.append((item[1], item[2]))

        if 'location' in search_dict:
            for item in operator_value_pairs:
                search_dict['location'].append(item)
        elif operator_value_pairs:
            search_dict['location'] = operator_value_pairs

        # remove locations from the query and return it
        input_query = re.sub(location_query, '', input_query, flags=re.I)
        return input_query

    def parse_for_category(self, input_query, search_dict):
        """ Parses input_query for a category search.
            Adds any category searches to search_dict.
            Returns the input_query with categories removed.
        """
        operator_value_pairs = list()
        category_search_patterns = re.findall(cat_query, input_query, re.I)

        # category_search_patterns = a list of ("cat", "=", value)
        for item in category_search_patterns:
            operator_value_pairs.append((item[1], item[2]))

        if 'category' in search_dict:
            for item in operator_value_pairs:
                search_dict['category'].append(item)
        elif operator_value_pairs:
            search_dict['category'] = operator_value_pairs

        # remove categorys from the query and return it
        input_query = re.sub(cat_query, '', input_query, flags=re.I)
        return input_query

    def parse_for_keyword(self, input_query, search_dict):
        """ Parses input_query for a keyword search.
            Adds any keyword searches to search_dict.
            Returns the input_query with keywords removed.
        """
        # strip all other query types from the input_query
        stripped_query = re.sub(date_query, '', input_query, flags=re.I)
        stripped_query = re.sub(price_query, '', stripped_query, flags=re.I)
        stripped_query = re.sub(location_query, '', stripped_query, flags=re.I)
        stripped_query = re.sub(cat_query, '', stripped_query, flags=re.I)
        keywords = stripped_query.split()

        operator_value_pairs = list()
        keyword_search_patterns = re.findall(term_query, stripped_query, re.I)

        # keyword_search_patterns = a list of (term, "%", "") or ("", "", term)
        for item in keyword_search_patterns:
            if item[1]:
                operator_value_pairs.append((item[1], item[0]))
            elif item[2]:
                operator_value_pairs.append(("=", item[2]))
            else:
                print("parse_for_keyword got messed up")

        if 'keyword' in search_dict:
            for item in operator_value_pairs:
                search_dict['keyword'].append(item)
        elif operator_value_pairs:
            search_dict['keyword'] = operator_value_pairs

        # remove keywords from the original query and return it
        for item in keywords:
            input_query = input_query.replace(item, "")
        return input_query