import datetime
import fileinput
import operator
import re

from bsddb3 import db

from common import AD_INDEX, TE_INDEX, PR_INDEX, DA_INDEX
from input_parser import InputParser

operators = {
    ">": operator.gt,  # works like operators[">"](a,b)
    "<": operator.lt,
    "=": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,  # Note: % not included as startswith uses a different call pattern
}


def check_multiple_equals(criteria):
    one = None
    for op, value_str in criteria:
        if one and op == "=" and one != value_str:
            return True
        if op == "=":
            one = value_str
    return False


def check_null_subset(criteria):
    one = None
    for op, value_str in criteria:
        if one and (op == "=" or op == ">" or op == "<") and one != value_str:
            return True
        if op == "=":
            one = value_str
    return False


def parse_date(date):
    """
    Converts a date string to a datetime.datetime object
    """
    try:
        year, month, day = date.split("/")
        return datetime.datetime(year=int(year), month=int(month), day=int(day))
    except Exception:
        raise ValueError("{} must follow: 'YYYY/MM/DD'".format(date))


def parse_price_range(criteria):
    """Returns lower and upper bounds as strings to use as comparisons in Berkeley databases"""
    num_of_spaces = 12  # See get_price_matches todo
    lower_bounds = None
    lower_bounds_operator = None
    upper_bounds = None
    upper_bounds_operator = None
    for op, value_str in criteria:
        value = int(value_str)
        if op in ("=", "<", "<="):
            if not upper_bounds or (int(upper_bounds) > value and upper_bounds_operator != "="):
                upper_bounds = value_str.rjust(num_of_spaces)
                upper_bounds_operator = op
            elif upper_bounds is value and upper_bounds_operator is "<=":
                upper_bounds_operator = op
            elif upper_bounds is value and upper_bounds_operator is "<" and op is "=":
                upper_bounds_operator = op
        if op in ("=", ">", ">="):
            if not lower_bounds or (int(lower_bounds) < value and lower_bounds_operator != "="):
                lower_bounds = value_str.rjust(num_of_spaces)
                lower_bounds_operator = op
            elif lower_bounds is value and lower_bounds_operator is ">=":
                lower_bounds_operator = op
            elif lower_bounds is value and lower_bounds_operator is ">" and op is "=":
                lower_bounds_operator = op

    return lower_bounds_operator, lower_bounds, upper_bounds_operator, upper_bounds


def parse_date_range(criteria):
    """Returns lower and upper bounds as strings to use as comparisons in Berkeley databases"""
    lower_bounds = None
    lower_bounds_operator = None
    upper_bounds = None
    upper_bounds_operator = None
    for op, value_str in criteria:
        value = parse_date(value_str)
        if op in ("=", "<", "<="):
            if not upper_bounds or (parse_date(upper_bounds) > value and upper_bounds_operator != "="):
                upper_bounds = value_str
                upper_bounds_operator = op
            elif upper_bounds is value and upper_bounds_operator is "<=":
                upper_bounds_operator = op
            elif upper_bounds is value and upper_bounds_operator is "<" and op is "=":
                upper_bounds_operator = op
        if op in ("=", ">", ">="):
            if not lower_bounds or (parse_date(lower_bounds) < value and lower_bounds_operator != "="):
                lower_bounds = value_str
                lower_bounds_operator = op
            elif lower_bounds is value and lower_bounds_operator is ">=":
                lower_bounds_operator = op
            elif lower_bounds is value and lower_bounds_operator is ">" and op is "=":
                lower_bounds_operator = op

    return lower_bounds_operator, lower_bounds, upper_bounds_operator, upper_bounds


class AdsDatabase:
    """Handles queries for ads using 4 Berkeley Database indexes"""

    def __init__(self, ad_filename=AD_INDEX, terms_filename=TE_INDEX,
                 dates_filename=DA_INDEX, prices_filename=PR_INDEX):
        """Initialize mode, databases, and cursors"""
        self.adsDB = db.DB()
        self.termsDB = db.DB()
        self.pdatesDB = db.DB()
        self.pricesDB = db.DB()
        self.adsDB.open(ad_filename, None, db.DB_HASH, db.DB_CREATE)
        self.termsDB.open(terms_filename, None, db.DB_BTREE, db.DB_CREATE)
        self.pdatesDB.open(dates_filename, None, db.DB_BTREE, db.DB_CREATE)
        self.pricesDB.open(prices_filename, None, db.DB_BTREE, db.DB_CREATE)
        self.ads_cursor = self.adsDB.cursor()
        self.terms_cursor = self.termsDB.cursor()
        self.dates_cursor = self.pdatesDB.cursor()
        self.price_cursor = self.pricesDB.cursor()
        self.mode = "brief"

    def __enter__(self):
        """Allows use of with"""
        return self

    def change_mode(self, line):
        if line.endswith("full"):
            self.mode = "full"
        elif line.endswith("brief"):
            self.mode = "brief"
        else:
            print("Invalid mode")

    def get_matching_terms(self, query):
        """
        Gets matching ad ids based on words in title and/or description
        :param query: InputParser.parse_input() dict
        :return: set of byte(ad ids)
        """
        results = set()
        search_results = set()
        for op, search in query["keyword"]:
            row = self.terms_cursor.set_range(search.encode("utf-8"))

            while row:
                if op is '%':
                    can_add = row[0].decode('utf-8').startswith(search)
                else:
                    can_add = row[0].decode('utf-8') == search

                if can_add:
                    # print(row)
                    search_results.add(row[1])
                else:
                    break
                row = self.terms_cursor.next()
            results = self.merge_results(results, search_results)
            search_results = set()
            if not results:
                break
        return results

    def get_matching_prices(self, query):
        """
        Gets matching ad ids based on price, ad id, category and location of the ad
        :param query: InputParser.parse_input() dict
        :return: set of byte(ad ids)
        """
        results = set()
        search_results = set()
        for op, search in query["price"]:
            search = search.rjust(12)
            print(op)
            print(search)
            if op in ("=", ">", ">="):
                row = self.price_cursor.set_range(search.encode("utf-8"))
            else:
                row = self.price_cursor.first()

            while row:

                price, data = row
                price = int(price.decode('utf-8'))
                aid, cat, loc = data.decode('utf-8').split(",")
                loc = loc.lower()
                cat = cat.lower()
                if operators[op](price, int(search)):
                    can_add = True
                    if "location" in query or "category" in query:
                        if "location" in query:
                            for op2, location in query["location"]:
                                if loc != location:
                                    can_add = False
                                    break
                        if "category" in query and can_add:
                            for op3, category in query["category"]:
                                if cat != category:
                                    can_add = False
                                    break
                    if can_add:
                        search_results.add(aid.encode("utf-8"))
                elif op in ("=", "<", "<="):
                    break
                row = self.price_cursor.next()
            if not search_results:
                return set()
            results = self.merge_results(results, search_results)
            search_results = set()
            if not results:
                return set()

        return results

    def get_matching_dates(self, query):
        """
        Gets matching ad ids based on date, ad id, category and location of the ad
        :param query: InputParser.parse_input() dict
        :return: set of byte(ad ids)
        """
        results = set()
        search_results = set()
        for op, search in query["date"]:
            if op in ("=", ">", ">="):
                row = self.dates_cursor.set_range(search.encode("utf-8"))
            else:
                row = self.dates_cursor.first()

            while row:

                date, data = row
                date = parse_date(date.decode('utf-8'))
                aid, cat, loc = data.decode('utf-8').split(",")
                loc = loc.lower()
                cat = cat.lower()
                if operators[op](date, parse_date(search)):
                    can_add = True
                    if "location" in query or "category" in query:
                        if "location" in query:
                            for op2, location in query["location"]:
                                if loc != location:
                                    can_add = False
                                    break
                        if "category" in query and can_add:
                            for op3, category in query["category"]:
                                if cat != category:
                                    can_add = False
                                    break
                    if can_add:
                        search_results.add(aid.encode("utf-8"))
                elif op in ("=", "<", "<="):
                    break
                row = self.dates_cursor.next()
            results = self.merge_results(results, search_results)
            if not results:
                break

        return results

    def print_matching_ads(self, query):
        """
        Gets matching ad ids based on category and/or location of the ad and prints them
        :param query: InputParser.parse_input() dict
        """
        had_a_result = False
        item = self.ads_cursor.first()
        while item:
            aid, ad = item
            ad = ad.decode("utf-8")
            can_add = True
            loc = re.search('<loc>(.*)</loc>', ad).group(1).lower()
            cat = re.search('<cat>(.*)</cat>', ad).group(1).lower()
            if "location" in query:
                for op, location in query["location"]:
                    if loc != location:
                        can_add = False
                        break
            if "category" in query and can_add:
                for op, category in query["category"]:
                    if cat != category:
                        can_add = False
                        break
            if can_add:
                had_a_result = True
                self.print_one_result(item)
            item = self.ads_cursor.next()

        if not had_a_result:
            print("No results")
        pass

    @staticmethod
    def merge_results(results1, results2):
        """
        Merges sets with intersection if they have values otherwise returns the one with values
        """
        if not results1:
            return results2
        if not results2:
            return results1
        return results1 & results2

    def execute(self, query):
        """
        Executes a query and prints the results according to mode
        :param query: dict of query conditions
        """
        results = set()
        if "price" in query:
            results = self.get_matching_prices(query)
            if not results:
                print("No results due to price restrictions")
                return

        if "date" in query:
            date_results = self.get_matching_dates(query)
            if not date_results:
                print("No results due to date restrictions")
                return
            results = self.merge_results(results, date_results)
            if not results:
                print("No results due to intersecting criteria between dates and prices")
                return

        if "keyword" in query:
            term_results = self.get_matching_terms(query)
            if not term_results:
                print("No results due to term restrictions")
                return
            results = self.merge_results(results, term_results)
            if not results:
                print("No results due to intersecting criteria terms and (prices and dates)")
                return

        if ("location" in query or "category" in query) and not \
                ("date" in query or "price" in query or "keyword" in query):
            print("Searching all ads. Queries like this one could be improved by making "
                  "location and category index files. This may take a while...")
            self.print_matching_ads(query)  # Loop through all ads looking for relevant ads
        else:
            self.print_results(results, query)

    def print_results(self, results, query):
        """
        Looks in ad.idx for the aids and prints either the whole ads or ad ids and titles based on mode
        :param query: InputParser.parse_input() dict
        :param results: set of byte(ad ids)
        """

        had_a_result = False
        for aid in results:
            can_add = True
            line = self.ads_cursor.set_range(aid)
            aid, ad = line
            ad = ad.decode("utf-8")
            if not ("date" in query or "price" in query) and ("location" in query or "category" in query):
                loc = re.search('<loc>(.*)</loc>', ad).group(1).lower()
                cat = re.search('<cat>(.*)</cat>', ad).group(1).lower()
                if "location" in query:
                    for op, location in query["location"]:
                        if loc != location:
                            can_add = False
                            break
                if "category" in query and can_add:
                    for op, category in query["category"]:
                        if cat != category:
                            can_add = False
                            break

            if line and can_add:
                had_a_result = True
                self.print_one_result(line)

        if not had_a_result:
            print("No results")

    def print_one_result(self, line):
        """
        Looks in ad.idx for the aid and prints either the whole ad or ad id and title based on mode
        :param line: one line from the ad.idx file
        """
        ad = str(line[1].decode("utf-8"))
        if self.mode is "full":
            print(ad)
        else:
            title = re.search('<ti>(.*)</ti>', ad).group(1)
            print(str(line[0].decode("utf-8")) + ": " + title)

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes databases and cursors"""
        self.ads_cursor.close()
        self.terms_cursor.close()
        self.dates_cursor.close()
        self.price_cursor.close()
        self.adsDB.close()
        self.termsDB.close()
        self.pdatesDB.close()
        self.pricesDB.close()


def phase3(file=None):
    with AdsDatabase() as ads_database:
        input_parser = InputParser()
        for line in fileinput.input(file):
            line = line.lower().strip()
            # print(line)
            if input_parser.validate_query(line):
                # print(input_parser.parse_input(line))
                ads_database.execute(input_parser.parse_input(line))
            elif line.startswith("output"):
                ads_database.change_mode(line)
            else:
                print("Invalid query")
                pass
            pass
        pass
    pass


if __name__ == "__main__":
    phase3()
    pass
