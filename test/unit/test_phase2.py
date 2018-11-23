""" Note that these aren't real tests since we don't have
    data to validate against
"""
import os
import mini_project_2
from mini_project_2.phase2 import sort_data, sort_all

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
ads_infile = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
ads_outfile = os.path.join(MINI_PROJECT_2_PATH, "data/sorted/ads.txt")

def test_sort_ads():
    sort_data(ads_infile, ads_infile)

if __name__ == "__main__":
    test_sort_ads()
    pass