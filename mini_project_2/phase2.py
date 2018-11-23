import subprocess
import os
import mini_project_2

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")

# command: sort inputfile.txt -u
def sort_all():
    sort_data(ads_file, ads_file)
    sort_data(terms_file, terms_file)
    sort_data(pdates_file, pdates_file)
    sort_data(prices_file, prices_file)

def sort_data(infile, outfile):
    command = ["sort", "-o", outfile, infile, "-u"]
    subprocess.run(command)