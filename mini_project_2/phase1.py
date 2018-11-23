import fileinput
import os
import re
import xml.etree.ElementTree as ET

import mini_project_2

MINI_PROJECT_2_PATH = os.path.dirname(os.path.realpath(mini_project_2.__file__))
ads_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-ads.txt")
terms_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-terms.txt")
pdates_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-pdates.txt")
prices_file = os.path.join(MINI_PROJECT_2_PATH, "data/10-prices.txt")


def write_ad(aid, line, filename=ads_file):
    """"""
    line = aid + ":" + line

    mode = 'a'  # append as already exists
    with open(filename, mode) as f:
        f.write(line)


def write_terms(root, filename=terms_file):
    """"""
    terms = list()
    pattern = re.compile(r'[0-9a-zA-Z_-]{3,}')
    remove_pattern = re.compile(r'&#(\\d)+;')
    replace_pattern = re.compile(r'&apos;|&quot;|&amp;')

    aid = root.find('aid').text

    title = root.find('ti').text
    title = re.sub(remove_pattern, '', title)
    title = re.sub(replace_pattern, ' ', title)
    title = title.lower().split(' ')

    desc = root.find('desc').text
    desc = re.sub(remove_pattern, '', desc)
    desc = re.sub(replace_pattern, ' ', desc)
    desc = desc.lower().split(' ')

    for word in title:
        for match in re.findall(pattern, word):
            terms.append(match + ":" + aid + '\n')

    for word in desc:
        for match in re.findall(pattern, word):
            terms.append(match + ":" + aid + '\n')

    mode = 'a'  # append as already exists
    with open(filename, mode) as f:
        for term in terms:
            f.write(term)


def write_price(root, filename=prices_file):
    """"""
    padding_length = 12
    price = root.find('price')
    if ET.iselement(price) and price.text:
        price = price.text.rjust(padding_length)
        aid = root.find('aid').text
        category = root.find('cat').text
        location = root.find('loc').text
        price_line = price + ":" + aid + "," + category + "," + location + "\n"

        mode = 'a'  # append as already exists
        with open(filename, mode) as f:
            f.write(price_line)


def write_pdate(root, filename=pdates_file):
    """"""
    pass


def is_ad_line(line):
    """"""
    return line.startswith("<ad>")


def generate_data_files(files=None):
    """"""

    os.makedirs(os.path.join(MINI_PROJECT_2_PATH, 'data'), exist_ok=True)
    with open(ads_file, 'w') as f:
        pass
    with open(prices_file, 'w') as f:
        pass
    with open(pdates_file, 'w') as f:
        pass
    with open(terms_file, 'w') as f:
        pass
    for line in fileinput.input(files=files):
        if not is_ad_line(line):
            continue

        root = ET.fromstring(line)
        aid = root.find('aid').text
        write_ad(aid, line)

        remove_pattern = re.compile(r'(&#[0-9]+;)')
        replace_pattern = re.compile(r'&apos;|&quot;|&amp;')
        line = re.sub(remove_pattern, '', line)
        line = re.sub(replace_pattern, ' ', line)

        root = ET.fromstring(line)
        write_price(root)
        write_terms(root)
        write_pdate(root)

    pass


if __name__ == '__main__':
    generate_data_files()
