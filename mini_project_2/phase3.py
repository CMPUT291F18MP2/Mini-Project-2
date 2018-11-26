import datetime
import operator
import re

from bsddb3 import db

from mini_project_2.common import AD_INDEX, TE_INDEX, PR_INDEX, DA_INDEX

operators = {
    ">": operator.gt,  # works like operators[">"](a,b)
    "<": operator.lt,
    "=": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
}


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
    """Returns lower and upper bounds as ints to use as comparisons in Berkeley databases"""
    lower_bounds = None
    lower_bounds_operator = None
    upper_bounds = None
    upper_bounds_operator = None
    for op, value in criteria:
        value = int(value)
        if op in ("=", "<", "<="):
            if not upper_bounds or upper_bounds > value:
                upper_bounds = value
                upper_bounds_operator = op
            elif upper_bounds is value and op is "<":
                upper_bounds_operator = op
        if op in ("=", ">", ">="):
            if not lower_bounds or lower_bounds < value:
                lower_bounds = value
                lower_bounds_operator = op
            elif lower_bounds is value and op is ">":
                lower_bounds_operator = op

    return lower_bounds_operator, lower_bounds, upper_bounds_operator, upper_bounds


def parse_date_range(criteria):
    """Returns lower and upper bounds as datetime.datetime objects to use as comparisons in Berkeley databases"""
    lower_bounds = None
    lower_bounds_operator = None
    upper_bounds = None
    upper_bounds_operator = None
    for op, value in criteria:
        value = parse_date(value)
        if op in ("=", "<", "<="):
            if not upper_bounds or upper_bounds > value:
                upper_bounds = value
                upper_bounds_operator = op
            elif upper_bounds is value and op is "<":
                upper_bounds_operator = op
        if op in ("=", ">", ">="):
            if not lower_bounds or lower_bounds < value:
                lower_bounds = value
                lower_bounds_operator = op
            elif lower_bounds is value and op is ">":
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
        for search in query["keyword"]:
            search_results = set()
            results = self.merge_results(results, search_results)
            if not results:
                break
        return results()

    def get_matching_prices(self, query):
        """
        Gets matching ad ids based on price, ad id, category and location of the ad
        :param query: InputParser.parse_input() dict
        :return: set of byte(ad ids)
        """
        results = set()
        can_add = True
        lower_bounds_operator, lower_bounds, upper_bounds_operator, upper_bounds = parse_price_range(query["price"])
        if lower_bounds:
            flag = db.DB_FIRST
            if lower_bounds_operator is ">":
                flag = db.DB_LAST
            row = self.price_cursor.get(lower_bounds, flag)
        else:
            row = self.price_cursor.first()

        while row:
            price, data = row
            price = int(price.decode('utf-8'))
            aid, cat, loc = data.decode('utf-8').split(",")

            if upper_bounds:
                if not operators[upper_bounds_operator](price, upper_bounds):
                    break

            if "location" in query or "category" in query:
                if "location" in query:
                    for op, location in query["location"]:
                        if loc is not location:
                            can_add = False
                            break
                if "category" in query and can_add:
                    for op, category in query["category"]:
                        if cat is not category:
                            can_add = False
                            break
            if can_add:
                results.add(aid.encode("utf-8"))
            row = self.price_cursor.next()
            can_add = True

        return results

    def get_matching_dates(self, query):
        """
        Gets matching ad ids based on date, ad id, category and location of the ad
        :param query: InputParser.parse_input() dict
        :return: set of byte(ad ids)
        """
        results = set()
        can_add = True
        lower_bounds_operator, lower_bounds, upper_bounds_operator, upper_bounds = parse_date_range(query["date"])
        if lower_bounds:
            flag = db.DB_FIRST
            if lower_bounds_operator is ">":
                flag = db.DB_LAST
            row = self.price_cursor.get(lower_bounds, flag)
        else:
            row = self.price_cursor.first()

        while row:
            date, data = row
            date = parse_date(date.decode('utf-8'))
            aid, cat, loc = data.decode('utf-8').split(",")

            if upper_bounds:
                if not operators[upper_bounds_operator](date, upper_bounds):
                    break

            if "location" in query or "category" in query:
                if "location" in query:
                    for op, location in query["location"]:
                        if loc is not location:
                            can_add = False
                            break
                if "category" in query and can_add:
                    for op, category in query["category"]:
                        if cat is not category:
                            can_add = False
                            break
            if can_add:
                results.add(aid.encode("utf-8"))
            row = self.price_cursor.next()
            can_add = True

        return results

    def print_matching_ads(self, query):
        """
        Gets matching ad ids based on category and/or location of the ad and prints them
        :param query: InputParser.parse_input() dict
        """
        had_a_result = False
        item = self.ads_cursor.first()
        while item:
            if not ("date" in query or "price" in query) and ("location" in query or "category" in query):
                can_add = True
                loc = ""  # TODO get loc from ads idx
                cat = ""  # TODO get cat from ads idx
                if "location" in query:
                    for op, location in query["location"]:
                        if loc is not location:
                            can_add = False
                            break
                if "category" in query and can_add:
                    for op, category in query["category"]:
                        if cat is not category:
                            can_add = False
                            break
                if can_add:
                    had_a_result = True
                    self.print_one_result(item)
            else:
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
                print("No results due to intersecting criteria")
                return

        if "keyword" in query:
            term_results = self.get_matching_terms(query)
            if not term_results:
                print("No results due to term restrictions")
                return
            results = self.merge_results(results, term_results)
            if not results:
                print("No results due to intersecting criteria")
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
        for aid in results:
            can_add = True
            line = self.ads_cursor.set(aid)
            if not ("date" in query or "price" in query) and ("location" in query or "category" in query):
                loc = ""  # TODO get loc from ads idx
                cat = ""  # TODO get cat from ads idx
                if "location" in query:
                    for op, location in query["location"]:
                        if loc is not location:
                            can_add = False
                            break
                if "category" in query and can_add:
                    for op, category in query["category"]:
                        if cat is not category:
                            can_add = False
                            break

            if line and can_add:
                self.print_one_result(line)

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


def phase3():
    with AdsDatabase() as ads_database:
        for line in input("Enter query: "):
            line = line.lower()
            if InputParser.validate_query(line):
                ads_database.execute(InputParser.parse_input(line))
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
