import fileinput
import os
import re
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


def write_terms(root, filename='data/terms.txt'):
    """"""
    # TODO: replace special characters with space: (&#\d\d\d)|(&quot)|(&apos)|(amp)
    terms = list()
    pattern = re.compile(r'[0-9a-zA-Z_-]{3,}')
    remove_pattern = re.compile(r'(&#(\\d)+;)')
    replace_pattern = re.compile(r'(&apos;)|(&quot;)|(&amp;)')

    aid = root.find('aid').text

    title = root.find('ti').text.lower()
    title = re.sub(remove_pattern, '', title)
    title = re.sub(replace_pattern, ' ', title)
    title = title.split(' ')

    desc = root.find('desc').text.lower()
    desc = re.sub(remove_pattern, '', desc)
    desc = re.sub(replace_pattern, ' ', desc)
    desc = desc.split(' ')
    print(desc)

    for word in title:
        for match in re.findall(pattern, word):
            terms.append(match + ":" + aid + '\n')

    for word in desc:
        for match in re.findall(pattern, word):
            terms.append(match + ":" + aid + '\n')

    if os.path.exists(filename):
        mode = 'a'  # append if already exists
    else:
        mode = 'w'  # make a new file if not
    with open(filename, mode) as f:
        for term in terms:
            f.write(term)


def write_price(root, filename='data/prices.txt'):
    """"""
    padding_length = 10
    price = root.find('price')
    if ET.iselement(price) and price.text:
        price = price.text.rjust(padding_length)
        aid = root.find('aid').text
        category = root.find('cat').text
        location = root.find('loc').text
        price_line = price + ":" + aid + "," + category + "," + location + "\n"

        if os.path.exists(filename):
            mode = 'a'  # append if already exists
        else:
            mode = 'w'  # make a new file if not
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
        write_price(root)
        write_terms(root)

    pass


if __name__ == '__main__':
    generate_data_files()
