#!/usr/bin/python3
import json
import os
from os.path import expanduser
import sys


class App:

    app_command = 'help'
    app_params = []

    def __init__(self):

        self.user_home_path = expanduser("~")
        self.config_file_path = os.path.join(self.user_home_path, '.lazura')

        try:
            self.config = open(self.config_file_path)
        except IOError as e:
            self.raise_error('Error: {}: {}'.format(self.config_file_path,
                                                    os.strerror(e.errno)))

        try:
            self.config_dict = json.loads(''.join(self.config.readlines()))
        except ValueError as e:
            self.raise_error('Error: {}: invalid JSON: {}'.format(self.config_file_path, e))

        # todo: config format validate

        self.parse_argv()
        self.run_command()

    def raise_error(self, message, final_func=None):
        print (message)
        print ('Aborted.')
        if final_func is not None:
            final_func()
        exit()

    def show_docs(self):
        print ('...help will be here...')
        exit()

    def parse_argv(self):
        sys.argv.pop(0)
        if len(sys.argv) == 0:
            sys.argv.insert(0, self.app_command)
        else:
            self.app_command = sys.argv[0]
            self.app_params = sys.argv[1:]

    def run_command(self):
        if self.app_command == 'help':
            self.show_docs()
        if self.app_command == 'commit':
            if not len(self.app_params):
                self.raise_error('Error: commit: param \'name\' is missing')
            self.action_commit(self.app_params[0])

    def action_commit(self, name=None):
        print (name)


if __name__ == "__main__":

    App()

    #
    # try:
    #     config_dict = json.loads(''.join(config.readlines()))
    # except ValueError as e:
    #     exit('Error: {}: invalid JSON: {}'.format(config_file_path, e))
    #
    # # todo: config format validate
    #
    # if len(sys.argv) == 1:
    #     show_help() and exit()
    #
    # elif len(sys.argv) >= 2:
    #     if sys.argv[1] == 'commit':
    #         try:
    #             goal = sys.argv[3]
    #         except IndexError:
    #             exit('Error: commit: name of source is missing')
    #
    #
    #
    #
    #
    #

