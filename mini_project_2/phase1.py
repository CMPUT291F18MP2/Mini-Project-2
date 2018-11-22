import fileinput
import os
import xml.etree.ElementTree as ET


def write_ad(aid, line, filename='data/ads.txt'):
    """"""
    line = aid + ":" + line

    if os.path.exists(filename):
        mode = 'a'  # append if already exists
    else:
        mode = 'w'  # make a new file if not
    with open(filename, mode) as f:
        f.write(line)


def write_term(root):
    """"""
    pass


def write_price(root):
    """"""
    price = root.find('price')
    if price and price.text:
        price = price.text
    else:
        price = '0'
    pass


def write_pdate(root):
    """"""
    pass


def is_ad_line(line):
    """"""
    return line.startswith("<ad>")


def generate_data_files(files=None):
    """"""
    for line in fileinput.input(files=files):
        if not is_ad_line(line):
            continue

        root = ET.fromstring(line)
        aid = root.find('aid').text
        print(root.find('price'))
        print(root.find('priced'))
        
        write_ad(aid, line)

    pass


if __name__ == '__main__':
    generate_data_files()
