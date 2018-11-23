import subprocess

# command: sort inputfile.txt -u
from mini_project_2.common import ads_file, terms_file, pdates_file, prices_file


def sort_all():
    sort_data(ads_file, ads_file)
    sort_data(terms_file, terms_file)
    sort_data(pdates_file, pdates_file)
    sort_data(prices_file, prices_file)


def sort_data(infile, outfile):
    command = ["sort", "-o", outfile, infile, "-u"]
    subprocess.run(command)