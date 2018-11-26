import fileinput
import os
import re
import xml.etree.ElementTree as ET

import mini_project_2

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/ads.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/terms.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/pdates.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/prices.txt")


def write_ad(aid, line, f):
    """"""
    line = aid + ":" + line

    f.write(line)


def write_terms(root, f):
    """"""
    terms = list()
    pattern = re.compile(r'[0-9a-zA-Z_-]{3,}')

    aid = root.find('aid').text

    title = root.find('ti').text
    if title:
        title = title.lower().split(' ')
        for word in title:
            for match in re.findall(pattern, word):
                terms.append(match + ":" + aid + '\n')

    desc = root.find('desc').text
    if desc:
        desc = desc.lower().split(' ')
        for word in desc:
            for match in re.findall(pattern, word):
                terms.append(match + ":" + aid + '\n')

    for term in terms:
        f.write(term)


def write_price(root, f):
    """"""
    padding_length = 12
    price = root.find('price')
    if ET.iselement(price) and price.text:
        price = price.text.rjust(padding_length)
        aid = root.find('aid').text
        category = root.find('cat').text
        location = root.find('loc').text
        price_line = price + ":" + aid + "," + category + "," + location + "\n"

        f.write(price_line)


def write_pdate(root, f):
    """"""
    pdate = root.find('date')
    if ET.iselement(pdate) and pdate.text:
        aid = root.find('aid').text
        category = root.find('cat').text
        location = root.find('loc').text
        pdate_line = pdate.text + ":" + aid + "," + category + "," + location + "\n"

        f.write(pdate_line)


def is_ad_line(line):
    """"""
    return line.startswith("<ad>")


def remove_special_chars(line):
    """"""
    remove_pattern = re.compile(r'(&#[0-9]+;)')
    replace_pattern = re.compile(r'&apos;|&quot;|&amp;')
    line = re.sub(remove_pattern, '', line)
    return re.sub(replace_pattern, ' ', line)


def generate_data_files(files=None):
    """"""
    if files:
        print(files)
    else:
        print("Using std_in")

    os.makedirs(os.path.join(MINI_PROJECT_2_PATH, 'data'), exist_ok=True)
    with open(ads_file, 'w') as f_ads:
        with open(prices_file, 'w') as f_prices:
            with open(pdates_file, 'w') as f_pdates:
                with open(terms_file, 'w') as f_terms:
                    for line in fileinput.input(files=files):
                        if not is_ad_line(line):
                            continue

                        root = ET.fromstring(line)
                        aid = root.find('aid').text
                        write_ad(aid, line, f_ads)

                        line = remove_special_chars(line)

                        root = ET.fromstring(line)
                        write_price(root, f_prices)
                        write_terms(root, f_terms)
                        write_pdate(root, f_pdates)

    pass


if __name__ == '__main__':
    generate_data_files()
