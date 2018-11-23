import subprocess


# command: sort inputfile.txt -u
def sort_all():
    sortData("ads.txt", "ads.txt")
    sortData("pdates.txt", "pdates.txt")
    sortData("prices.txt", "prices.txt")
    sortData("terms.txt", "terms.txt")

def sort_data(infile, outfile):
    command = ["sort", "-o", outfile, infile, "-u"]
    subprocess.run(command)