#!/usr/bin/python3.5
'''
Script for concatenating .saz files (Fiddler specific zip archives).
WARNING: the script currently does not support captures with WebSocket messages.
Currently a Linux only implementation.

Following: http://fiddler.wikidot.com/saz-files
'''

from zipfile import ZipFile
import os, os.path
import argparse
import shutil
import time
import json
import colorama
import subprocess

class Sazcat:

    DST = os.path.expanduser("~/sazcat/")
    NEW = os.path.expanduser("~/sazcat/output/")
    NEW_SAZ = DST + "out"
    META_FORMAT = "[Content_Types].xml"
    confidential_strings = "/home/adobre/scripts/confidential_strings.json"
    ID = 0
    C = 0
    M = 1
    S = 2
    W = 3

    def __init__(self, files, check, output='out.saz'):
        self.files = files
        self.dir_map = {}
        self.do_check = check

    def list_files(self):
        for file in self.files:
            with ZipFile(file) as saz_file:
                print(saz_file.printdir())

    def __current_id(self):
        self.ID += 1
        return self.ID

    def concatenate(self):
        self.__unpack()
        self.__merge()
        self.__repack()

    '''
    Unzip each .saz file.
    '''
    def __unpack(self):
        self.capture_files = 0
        for file in self.files:
            with ZipFile(file) as saz_file:
                file_name = file.split('/')[-1]
                self.dir_map[self.ID] = file_name.split('.saz')[0]
                self.ID += 1
                saz_file.extractall(self.DST + file_name.split('.saz')[0])
                self.capture_files += (len([x for x in saz_file.namelist() if "raw/" in x]) - 1)
        self.capture_files /= 3
        print("Total files: ", self.capture_files)

    def __string_check(self):
        pass
        # with open(self.confidential_strings) as secret:
        #     data = json.load(secret)
        #     print(data["strings"])
        #     for string in data["strings"]:
        #         print("grep -rn " + string + " " + str(os.getcwd()))
        #         subprocess.Popen("grep -rn " + string + " " + str(os.getcwd()),
        #             stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    '''
    Bring together all files form the 'raw' directories and rename them.
    '''
    def __merge(self):
        shutil.rmtree(self.NEW, ignore_errors=True)
        os.makedirs(self.NEW + 'raw/')
        offset = 0
        name_format = "{:1}"
        if self.capture_files > 999:
            name_format = "{:04}"
        elif self.capture_files > 99:
            name_format = "{:03}"
        elif self.capture_files > 9:
            name_format = "{:02}"

        os.chdir(self.DST + self.dir_map[0])
        os.rename(self.META_FORMAT, self.NEW + self.META_FORMAT)
        for dir_id in range(0, self.ID):
            current_path = self.DST + self.dir_map[dir_id] + '/raw/'
            os.chdir(current_path)
            if self.do_check:
                self.__string_check()
            fl = sorted(os.listdir(current_path))
            sessions = [fl[i:i+3] for i in range(0, len(fl), 3)]
            for session in sessions:
                os.rename(session[Sazcat.C], self.NEW + 'raw/' + name_format.format(
                    offset + int(session[Sazcat.C].split('_')[0])) + '_c.txt')
                os.rename(session[Sazcat.M], self.NEW + 'raw/' + name_format.format(
                    offset + int(session[Sazcat.M].split('_')[0])) + '_m.xml')
                os.rename(session[Sazcat.S], self.NEW + 'raw/' + name_format.format(
                    offset + int(session[Sazcat.S].split('_')[0])) + '_s.txt')
            offset += len(sessions)
            print("offset after", self.dir_map[dir_id], ":\t", offset)
            shutil.rmtree(self.DST + self.dir_map[dir_id])

    '''
    Create a zip archive of the new merged 'raw' directory. The extra files are
    copied from the first .saz file.
    '''
    def __repack(self):
        try:
            os.remove(self.NEW_SAZ)
        except:
            pass
        os.chdir(self.NEW + 'raw/')
        shutil.make_archive(self.NEW_SAZ, 'zip', self.NEW)
        os.rename(self.NEW_SAZ + '.zip', self.NEW_SAZ + '.saz')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', type=str, nargs='+', help="list of space sperated saz file names")
    parser.add_argument('-l', '--list', dest='list_display', action='store_true')
    parser.add_argument('-c', '--check', dest='check_strings', action='store_true')
    parser.add_argument('-o', '--outputfile', type=str, default='out.saz', help="optional output file name, defaults to out.saz")

    parser.set_defaults(list_display=False, check_strings=False)
    args = parser.parse_args()
    cat = Sazcat(files=args.filenames, output=args.outputfile, check=args.check_strings)
    if args.list_display:
        cat.list_files()
    cat.concatenate()

if __name__ == "__main__":
    main()
