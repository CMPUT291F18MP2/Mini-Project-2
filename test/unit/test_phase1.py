import os

import mini_project_2
from mini_project_2.phase1 import is_ad_line, generate_data_files

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
small_input_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10.txt")
small_ads_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-ads.txt")
small_terms_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-terms.txt")
small_pdates_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-pdates.txt")
small_prices_file = os.path.join(MINI_PROJECT_2_PATH, "smallTestData/10-prices.txt")

ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-ads.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-terms.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-pdates.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-prices.txt")


def test_is_ad_line():
    print(small_input_file)
    assert is_ad_line("<ad>")
    assert not is_ad_line("<ad")


def test_generate_ads_files():
    generate_data_files(small_input_file)
    assert open(small_ads_file).read() == open('data/ads.txt').read()


def test_generate_prices_files():
    generate_data_files(small_input_file)
    assert open(small_prices_file).read() == open('data/prices.txt').read()


def test_generate_pdates_files():
    generate_data_files(small_input_file)
    assert open(small_pdates_file).read() == open('data/pdates.txt').read()


def test_generate_terms_files():
    generate_data_files(small_input_file)
    assert open(small_terms_file).read() == open('data/terms.txt').read()


def test_generate_data_files():  # todo: kinda slow; speed it up somehow?
    generate_data_files(os.path.abspath("../1000TestData/1k.txt"))
    assert open('../1000TestData/1k-ads.txt').read() == open('data/ads.txt').read()
    assert open('../1000TestData/1k-prices.txt').read() == open('data/prices.txt').read()
    assert open('../1000TestData/1k-terms.txt').read() == open('data/terms.txt').read()
    assert open('../1000TestData/1k-pdates.txt').read() == open('data/pdates.txt').read()
