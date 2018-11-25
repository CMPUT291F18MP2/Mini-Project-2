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

    def __enter__(self):
        return self

    def get_matching_prices(self, query):
        return set()

    def get_matching_terms(self, query):
        return set()

    def get_matching_dates(self, query):
        return set()

    @staticmethod
    def merge_results(*results):
        """Merges sets with intersection if they have values"""
        intersection = set()
        for result in results:
            if result:
                if not intersection:
                    intersection = result
                else:
                    intersection = intersection & result
        return intersection

    def execute(self, query):
        """
        Executes a query
        :param query: dict of query conditions
        :return: results from the query as a set
        """
        results = set()
        price_results = date_results = term_results = set()
        if "price" in query:
            price_results = self.get_matching_prices(query)
        if "date" in query:
            date_results = self.get_matching_dates(query)
        if "keyword" in query:
            term_results = self.get_matching_terms(query)
        if ("location" in query or "category" in query) and not \
                ("date" in query or "price" in query or "keyword" in query):
            print("Searching all ads. Queries like this one could be improved by making "
                  "location and category index files. This may take a while...")
            pass  # Loop through all ads looking for relevant ads

        results = self.merge_results(price_results, date_results, term_results)

        return results

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
