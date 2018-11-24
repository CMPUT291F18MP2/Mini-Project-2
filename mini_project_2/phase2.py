import subprocess
import os

from mini_project_2.common import ads_file, terms_file, pdates_file, prices_file


def sort_all():
    os.system("sort -u < " + ads_file + " | ./break.pl | db_load -T -t hash ad.idx")
    os.system("sort -u < " + terms_file + " | ./break.pl | db_load -T -t btree te.idx")
    os.system("sort -u < " + pdates_file + " | ./break.pl | db_load -T -t btree da.idx")
    os.system("sort -u < " + prices_file + " | ./break.pl | db_load -T -t btree pr.idx")


def sort_data(infile, outfile):
    command = ["sort", "-o", outfile, infile, "-u"]
    subprocess.run(command)