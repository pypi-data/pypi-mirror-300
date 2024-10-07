from utils.connection import connect_liboffice
from utils.cleanup import clean_up

from core import document
from core import sheet
from core import range

from core.state import opened_docs as od

files_to_create = [["scratch.ods", "Calc"], ["template.ods", "Calc"]]
files_to_open = [] # looks for files in workdir/input


def main():
    connect_liboffice()
    # write your code here
    # or as a package, import what you need for your own project
    clean_up()

if __name__ == '__main__':
    # main()
    ...


