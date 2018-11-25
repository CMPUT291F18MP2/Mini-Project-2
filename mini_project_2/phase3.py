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

    def get_matching_prices(self, query):
        """
        Gets matching ad ids based on price, ad id, category and location of the ad
        :param query:
        :return: set of byte(ad ids)
        """
        return set()

    def get_matching_terms(self, query):
        """
        Gets matching ad ids based on words in title and/or description
        :param query:
        :return: set of byte(ad ids)
        """
        return set()

    def get_matching_dates(self, query):
        """
        Gets matching ad ids based on date, ad id, category and location of the ad
        :param query:
        :return: set of byte(ad ids)
        """
        return set()

    def print_matching_ads(self, query):
        """
        Gets matching ad ids based on category and/or location of the ad and prints them
        :param query:
        """

        if self.mode is "full":
            print(str(None.decode("utf-8")))  # TODO replace none
        else:
            print(str(None.decode("utf-8")))
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
        elif self.mode is "full":
            self.print_ads_from_aids(results)
        else:
            for aid in results:
                print(str(aid.decode("utf-8")))

    def print_ads_from_aids(self, results):
        for aid in results:
            print(str(self.ads_cursor.get(aid).decode("utf-8")))

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
