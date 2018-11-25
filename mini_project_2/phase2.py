import subprocess
import os
import mini_project_2

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))

database_path = os.path.join(MINI_PROJECT_2_PATH, "database")

break_pl = os.path.join(MINI_PROJECT_2_PATH, "break.pl")

ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")

ads_formatted = os.path.join(MINI_PROJECT_2_PATH, "data/ads_formatted.txt")
terms_formatted = os.path.join(MINI_PROJECT_2_PATH, "data/terms_formatted.txt")
pdates_formatted = os.path.join(MINI_PROJECT_2_PATH, "data/pdates_formatted.txt")
prices_formatted = os.path.join(MINI_PROJECT_2_PATH, "data/prices_formatted.txt")

ads_db = os.path.join(MINI_PROJECT_2_PATH, "database/ad.idx")
terms_db = os.path.join(MINI_PROJECT_2_PATH, "database/te.idx")
pdates_db = os.path.join(MINI_PROJECT_2_PATH, "database/da.idx")
prices_db = os.path.join(MINI_PROJECT_2_PATH, "database/pr.idx")

# command: sort inputfile.txt -u
def sort_all():
    sort_data(ads_file, ads_file)
    sort_data(terms_file, terms_file)
    sort_data(pdates_file, pdates_file)
    sort_data(prices_file, prices_file)

def sort_data(infile, outfile):
    command = ["sort", "-o", outfile, infile, "-u"]
    subprocess.run(command)

def format_data_file(infile, outfile):
    """ Formats a data file into a format that db_load expects.
        Keys appear in one line followed by their data and so on.
        Backslashes are removed.

        Note that outfile can not be the same as infile.

        The linux command is:
            perl break.pl < infile > outfile
    """
    assert infile is not outfile, "Cannot overwrite existing file!"
    # subprocess.run() isn't working here and I'm not sure why.
    # command = ["perl", break_pl, "<", infile, ">", outfile]
    # subprocess.run(command)
    os.system("perl " + break_pl + " < " + infile + " > " + outfile)

def format_all():
    format_data_file(ads_file, ads_formatted)
    format_data_file(terms_file, terms_formatted)
    format_data_file(pdates_file, pdates_formatted)
    format_data_file(prices_file, prices_formatted)

def db_load(infile, outfile, db_type):
    """ Calls the linux db_load command to load up the database files

        The command is:
            db_load -c duplicates=1, -f infile -T
            -t [ btree | hash | queue | recno ] outfile
    """
    assert db_type is "btree" or db_type is "hash" or \
                db_type is "queue" or db_type is "recno"
    # command = ["db_load", "-c", "duplicates=1", "-f", infile,
    #                 "-T", "-t", db_type, outfile]
    # subprocess.run(command)
    if os.path.exists(outfile):
        os.remove(outfile)
    os.system("db_load -c duplicates=1 -f " + infile +
                     " -T -t " + db_type + " " + outfile)

def db_load_all():
    if not os.path.exists(database_path):
        os.makedirs(database_path)
    db_load(ads_formatted, ads_db, "hash")
    db_load(terms_formatted, terms_db, "btree")
    db_load(pdates_formatted, pdates_db, "btree")
    db_load(prices_formatted, prices_db, "btree")

if __name__ == "__main__":
    format_all()
    pass
