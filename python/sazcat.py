#!/usr/bin/python3.5

from zipfile import ZipFile
import os, os.path
import argparse

class Sazcat:

    DST = "/tmp/sazcat/"
    ID = 0

    def __init__(self, files):
        self.files = files
        self.dir_map = {}

    def list_files(self):
        for file in self.files:
            with ZipFile(file) as saz_file:
                # print(saz_file.namelist())
                print(saz_file.printdir())

    def __current_id(self):
        self.ID += 1
        return self.ID

    def concatenate(self):
        self.__unpack()
        self.__merge()
        self.__repack()

    def __unpack(self):
        for file in self.files:
            with ZipFile(file) as saz_file:
                file_name = file.split('/')[-1]
                self.dir_map[self.ID] = file_name
                self.ID += 1
                saz_file.extractall(self.DST + file_name)

    def __merge(self):
        total_files = 0
        for dir_id in range(0, self.ID):
            print(os.listdir(self.DST + self.dir_map[dir_id] + '/raw/'))


        #     total_files += len(os.listdir(self.dir_map[dir_id]))

    def __repack(self):
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', type=str, nargs='+', help="list of space sperated saz file names")
    parser.add_argument('-l', '--list', dest='list_display', action='store_true')
    parser.add_argument('-o', '--outputfile', type=str, default='out.saz', help="optional output file name, defaults to out.saz")
    parser.set_defaults(list_display=False)
    args = parser.parse_args()
    cat = Sazcat(files=args.filenames)
    if args.list_display:
        cat.list_files()
    cat.concatenate()
    print(args.outputfile)

if __name__ == "__main__":
    main()
