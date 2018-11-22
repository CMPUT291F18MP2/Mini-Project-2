import fileinput
import xml.etree.ElementTree as ET


def write_ad(root):
    """"""
    pass


def write_term(root):
    """"""
    pass


def write_price(root):
    """"""
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
        print(root.tag)
        print(root.text)
        for child in root:
            print(child.tag)
            print(child.text)
        write_ad(root)

    pass


if __name__ == '__main__':
    generate_data_files()
