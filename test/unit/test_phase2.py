import os
import mini_project_2
from mini_project_2.phase2 import sort_data, sort_all

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))

ads_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-ads-sorted.txt")
prices_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-prices-sorted.txt")
pdates_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-pdates-sorted.txt")
terms_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/sorted/1k-terms-sorted.txt")

ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")

def test_sort_ads():
    sort_data(ads_file, ads_file)
    assert open(ads_sorted_file).read() == open(ads_file).read()

def test_sort_all():
    sort_all()
    assert open(ads_sorted_file).read() == open(ads_file).read()
    assert open(prices_sorted_file).read() == open(prices_file).read()
    assert open(pdates_sorted_file).read() == open(pdates_file).read()
    assert open(terms_sorted_file).read() == open(terms_file).read()

if __name__ == "__main__":
    test_sort_all()
    pass