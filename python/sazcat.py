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
        self.capture_files = 0
        for file in self.files:
            with ZipFile(file) as saz_file:
                file_name = file.split('/')[-1]
                self.dir_map[self.ID] = file_name
                self.ID += 1
                saz_file.extractall(self.DST + file_name)
                self.capture_files += (len([x for x in saz_file.namelist() if "raw/" in x]) - 1)
        self.capture_files /= 3
        print("Total files: ", self.capture_files)

    def __merge(self):
        offset = 0
        name_format = "{:1}"
        if self.capture_files > 9:
            name_format = "{:02}"
        elif self.capture_files > 99:
            name_format = "{:03}"
        elif self.capture_files > 999:
            name_format = "{:04}"

        for dir_id in range(0, self.ID):
            fl = sorted(os.listdir(self.DST + self.dir_map[dir_id] + '/raw/'))
            sessions = [fl[i:i+3] for i in range(0, len(fl), 3)]
            # print(sessions)
            for session in sessions:
                print(name_format.format(int(session[0].split('_')[0])))
            file_count = len(os.listdir(self.DST + self.dir_map[dir_id] + '/raw/'))
            offset += file_count

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
