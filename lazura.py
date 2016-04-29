#!/usr/bin/python3
import json
import os
from os.path import expanduser
import sys

import shutil

import datetime

from helper import get_dir_size, copy_anything


class App:

    app_command = 'help'
    app_params = []

    def __init__(self):

        self.user_home_path = expanduser("~")
        self.config_file_path = os.path.join(self.user_home_path, '.lazura')

        try:
            self.config_raw = open(self.config_file_path)
        except IOError as e:
            self.raise_error('Error: {}: {}'.format(self.config_file_path,
                                                    os.strerror(e.errno)))

        try:
            self.config = json.loads(''.join(self.config_raw.readlines()))
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

    def node_exists(self, node_name):
        return True if node_name in self.config else False

    def node_exists_or_error(self, node_name):
        if not self.node_exists(node_name):
            self.raise_error('Error: node \'{}\' is not exists'
                             .format(node_name))

    def get_node_param(self, node_name, param_name):
        self.node_exists_or_error(node_name)
        try:
            return self.config[node_name][param_name]
        except KeyError:
            self.raise_error('Error: node \'{}\': param \'{}\' is missing'
                             .format(node_name, param_name))

    def action_commit(self, node_name):
        location = self.get_node_param(node_name, 'location')
        if not os.path.exists(location):
            self.raise_error('Error: node \'{}\': location \'{}\' is not exists'
                             .format(node_name, location))

        location_size = get_dir_size(location)

        destination = self.get_node_param(node_name, 'destination')
        if not os.path.exists(destination):
            self.raise_error('Error: node \'{}\': destination \'{}\' is not exists'
                             .format(node_name, destination))
        subdir = str(datetime.datetime.utcnow())
        destination_final_path = os.path.join(destination,
                                              os.path.basename(location),
                                              subdir,
                                              os.path.basename(location))

        print ('{}: saving...'.format(node_name))

        copy_anything(location, destination_final_path)

        if location_size == get_dir_size(destination_final_path):
            print ('SUCCESS.')
        else:
            print ('FAILED: Copying error')

if __name__ == "__main__":

    App()
