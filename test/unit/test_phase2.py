import os
import mini_project_2
from mini_project_2.common import ads_file, prices_file, pdates_file, terms_file
from mini_project_2.phase1 import generate_data_files
from mini_project_2.phase2 import sort_data, sort_all

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))

ads_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-ads-sorted.txt")
prices_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-prices-sorted.txt")
pdates_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-pdates-sorted.txt")
terms_sorted_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-terms-sorted.txt")

med_input_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k.txt")


def test_sort_all():
    generate_data_files(med_input_file)
    sort_all()
    assert open(ads_sorted_file).read() == open(ads_file).read()
    assert open(prices_sorted_file).read() == open(prices_file).read()
    assert open(pdates_sorted_file).read() == open(pdates_file).read()
    assert open(terms_sorted_file).read() == open(terms_file).read()


if __name__ == "__main__":
    test_sort_all()
    pass
