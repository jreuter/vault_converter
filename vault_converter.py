#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

"""
Program to convert one CSV vault export to another.  Current version only converts csv exported from the pwsafe
gorilla application to a bitwarden csv.

Usage:
    vault_converter [options] <file>
    vault_converter -h | --help
    vault_converter --version

Options:
    -h --help       Show this screen.
    --version       Show version.
    -q              Quiet the logging to only ERROR level.
    -v              Verbose output (INFO level).
    -s              Queue up and Split videos.
    --debug         Very Verbose output (DEBUG level).
"""
import os, sys, csv
from docopt import docopt
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s %(levelname)s %(message)s')

class VaultConverter:
    _arguments = None
    _log_level = 'WARN'
    _file = ''

    def __init__(self):
        """
        Gets command line arguments using docopt and sets logging level.
        """
        self._arguments = docopt(__doc__, version='0.1')
        self._set_logging_verbosity()

    def _set_logging_verbosity(self):
        """
        Sets the logging level based on arguments passed in the cli.
        """
        if self._arguments['-v']:
            self._log_level = logging.INFO
        if self._arguments['--debug']:
            self._log_level = logging.DEBUG
        if self._arguments['-q']:
            self._log_level = logging.ERROR
        logging.basicConfig(level=self._log_level,
                            format='%(asctime)s %(message)s')

    def main(self):
        self._file = self._arguments['<file>']
        output_rows = []
        output_fieldnames = ["folder", "favorite", "type", "name", "notes", "fields", "reprompt", "login_uri", "login_username", "login_password", "login_totp"]
        print(self._file)
        with open(self._file) as csvfile:
            # print("File is open")
            reader = csv.DictReader(csvfile)
            print("file has been read")
            # print(reader)
            for row in reader:
                output_row = {
                    "folder": row['group'].replace('/', '-').replace('.', '/'),
                    "favorite": "",
                    "type": "login",
                    "name": row['title'],
                    "notes": row['notes'],
                    "fields": "",
                    "reprompt": "",
                    "login_uri": row['url'],
                    "login_username": row['user'],
                    "login_password": row['password'],
                    "login_totp": ""
                }
                # print(dict(row))
                print(dict(output_row))
                # print(row['group'], row['title'], row['user'])
                output_rows.append(output_row)

        with open('converted_file.csv', 'w') as file:
            writer = csv.DictWriter(file, fieldnames=output_fieldnames)
            writer.writeheader()
            for row in output_rows:
                writer.writerow(row)


if __name__ == '__main__':
    VaultConverter().main()
