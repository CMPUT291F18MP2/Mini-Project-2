import filecmp
import os

from mini_project_2.phase1 import is_ad_line, generate_data_files

os.path.abspath("../smallTestData/10.txt")


def test_is_ad_line():
    assert is_ad_line("<ad>")
    assert not is_ad_line("<ad")


def test_generate_data_files():
    generate_data_files(os.path.abspath("../smallTestData/10.txt"))
    assert open('../smallTestData/10-ads.txt').read() == open('data/ads.txt').read()
    assert open('../smallTestData/10-terms.txt').read() == open('data/terms.txt').read()
    assert open('../smallTestData/10-prices.txt').read() == open('data/prices.txt').read()
    assert open('../smallTestData/10-pdates.txt').read() == open('data/pdates.txt').read()
