import fileinput
import os
import re
import xml.etree.ElementTree as ET


def write_ad(aid, line, filename='data/ads.txt'):
    """"""
    line = aid + ":" + line

    mode = 'a'  # append as already exists
    with open(filename, mode) as f:
        f.write(line)


def write_terms(root, filename='data/terms.txt'):
    """"""
    # TODO: replace special characters with space: (&#\d\d\d)|(&quot)|(&apos)|(amp)
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


def write_price(root, filename='data/prices.txt'):
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


def write_pdate(root):
    """"""
    pass


def is_ad_line(line):
    """"""
    return line.startswith("<ad>")


def generate_data_files(files=None):
    """"""

    os.makedirs('data', exist_ok=True)
    filename = 'data/ads.txt'
    with open(filename, 'w') as f:
        pass
    filename = 'data/prices.txt'
    with open(filename, 'w') as f:
        pass
    filename = 'data/pdates.txt'
    with open(filename, 'w') as f:
        pass
    filename = 'data/terms.txt'
    with open(filename, 'w') as f:
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
