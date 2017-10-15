#!/usr/bin/python3.5

from zipfile import ZipFile
import argparse

class Sazcat:

    def __init__(self, files):
        self.files = files

    def list_files(self):
        for file in self.files:
            with ZipFile(file) as saz_file:
                # print(saz_file.namelist())
                print(saz_file.printdir())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', type=str, nargs='+', help="list of space sperated saz file names")
    parser.add_argument('-l', '--list', dest='list_display', action='store_true')
    parser.set_defaults(list_display=False)
    args = parser.parse_args()
    cat = Sazcat(files=args.filenames)
    if args.list_display:
        cat.list_files()

if __name__ == "__main__":
    main()


