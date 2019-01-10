import os
import mini_project_2
from mini_project_2.phase2 import sort_data, sort_all, format_all, db_load_all

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))

ads_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-ads-sorted.txt")
prices_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-prices-sorted.txt")
pdates_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-pdates-sorted.txt")
terms_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-terms-sorted.txt")

ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")

ads_formatted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/formatted/1k-ads-formatted.txt")
prices_formatted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/formatted/1k-prices-formatted.txt")
pdates_formatted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/formatted/1k-pdates-formatted.txt")
terms_formatted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/formatted/1k-terms-formatted.txt")

ads_formatted_actual = os.path.join(MINI_PROJECT_2_PATH, "data/ads_formatted.txt")
prices_formatted_actual = os.path.join(MINI_PROJECT_2_PATH, "data/prices_formatted.txt")
pdates_formatted_actual = os.path.join(MINI_PROJECT_2_PATH, "data/pdates_formatted.txt")
terms_formatted_actual = os.path.join(MINI_PROJECT_2_PATH, "data/terms_formatted.txt")

ads_idx = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/idx/1k-ad.idx")
prices_idx = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/idx/1k-pr.idx")
pdates_idx = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/idx/1k-da.idx")
terms_idx = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/idx/1k-te.idx")

ads_db = os.path.join(MINI_PROJECT_2_PATH, "database/ad.idx")
terms_db = os.path.join(MINI_PROJECT_2_PATH, "database/te.idx")
pdates_db = os.path.join(MINI_PROJECT_2_PATH, "database/da.idx")
prices_db = os.path.join(MINI_PROJECT_2_PATH, "database/pr.idx")

/*
def test_sort_ads():
    sort_data(ads_file, ads_file)
    assert open(ads_sorted_file).read() == open(ads_file).read()

def test_sort_all():
    sort_all()
    assert open(ads_sorted_file).read() == open(ads_file).read()
    assert open(prices_sorted_file).read() == open(prices_file).read()
    assert open(pdates_sorted_file).read() == open(pdates_file).read()
    assert open(terms_sorted_file).read() == open(terms_file).read()

def test_format_all():
    format_all()
    assert open(ads_formatted_file).read() == open(ads_formatted_actual).read()
    assert open(prices_formatted_file).read() == open(prices_formatted_actual).read()
    assert open(pdates_formatted_file).read() == open(pdates_formatted_actual).read()
    assert open(terms_formatted_file).read() == open(terms_formatted_actual).read()

def test_db_load_all():
    db_load_all()
    # I'm not sure if the below assert statements actually work as intended...
    # assert open(ads_idx).read() == open(ads_db).read()
    # assert open(prices_idx).read() == open(prices_db).read()
    # assert open(pdates_idx).read() == open(pdates_db).read()
    # assert open(terms_idx).read() == open(terms_db).read()
*/
if __name__ == "__main__":
    test_sort_all()
    test_format_all()
    test_db_load_all()
    pass
