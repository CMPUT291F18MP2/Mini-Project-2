import os

import mini_project_2
from mini_project_2.phase1 import is_ad_line, generate_data_files

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
small_input_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10.txt")
small_ads_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-ads.txt")
small_terms_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-terms.txt")
small_pdates_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-pdates.txt")
small_prices_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-prices.txt")

med_input_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k.txt")
med_ads_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-ads.txt")
med_terms_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-terms.txt")
med_pdates_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-pdates.txt")
med_prices_file = os.path.join(MINI_PROJECT_2_PATH, "1000TestData/1k-prices.txt")

ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")


def test_is_ad_line():
    assert is_ad_line("<ad>")
    assert not is_ad_line("<ad")


def test_generate_ads_files():
    generate_data_files(small_input_file)
    assert open(small_ads_file).read() == open(ads_file).read()


def test_generate_prices_files():
    generate_data_files(small_input_file)
    assert open(small_prices_file).read() == open(prices_file).read()


def test_generate_pdates_files():
    generate_data_files(small_input_file)
    assert open(small_pdates_file).read() == open(pdates_file).read()


def test_generate_terms_files():
    generate_data_files(small_input_file)
    assert open(small_terms_file).read() == open(terms_file).read()


def test_generate_data_files():  # todo: kinda slow; speed it up somehow?
    generate_data_files(med_input_file)
    assert open(med_ads_file).read() == open(ads_file).read()
    assert open(med_prices_file).read() == open(prices_file).read()
    assert open(med_terms_file).read() == open(terms_file).read()
    assert open(med_pdates_file).read() == open(pdates_file).read()
