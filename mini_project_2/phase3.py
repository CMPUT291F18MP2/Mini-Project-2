import re

from bsddb3 import db

from mini_project_2.common import AD_INDEX, TE_INDEX, PR_INDEX, DA_INDEX


class AdsDatabase:

    adsDB = db.DB()
    termsDB = db.DB()
    pdatesDB = db.DB()
    pricesDB = db.DB()

    def __init__(self, ad_filename=AD_INDEX, terms_filename=TE_INDEX,
                 dates_filename=DA_INDEX, prices_filename=PR_INDEX):
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
        return self

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
        for search in query["price"]:
            search_results = set()
            results = self.merge_results(results, search_results)
            if not results:
                break
        return results()

    def get_matching_dates(self, query):
        """
        Gets matching ad ids based on date, ad id, category and location of the ad
        :param query: InputParser.parse_input() dict
        :return: set of byte(ad ids)
        """
        results = set()
        for search in query["date"]:
            search_results = set()
            results = self.merge_results(results, search_results)
            if not results:
                break
        return results()

    def print_matching_ads(self, query):
        """
        Gets matching ad ids based on category and/or location of the ad and prints them
        :param query: InputParser.parse_input() dict
        """
        had_a_result = False
        item = self.ads_cursor.first()
        while iter:
            if True:  # TODO check matches
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
            self.print_results(results)

    def print_results(self, results):
        """
        Looks in ad.idx for the aids and prints either the whole ads or ad ids and titles based on mode
        :param results: set of byte(ad ids)
        """
        for aid in results:
            line = self.ads_cursor.set(aid)
            if line:
                self.print_one_result(line)
            else:
                print("Note: btree files have an ad index that's not in ad.inx")

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
            if InputParser.validate_query(line):
                ads_database.execute(InputParser.parse_input(line))
            else:
                print("Invalid query")
                pass
            pass
        pass
    pass


if __name__ == "__main__":
    phase3()
    pass
