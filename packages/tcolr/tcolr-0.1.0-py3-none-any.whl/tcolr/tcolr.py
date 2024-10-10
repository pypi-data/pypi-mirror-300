#!/usr/bin/env python3
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import sys
import subprocess
import json
import os.path
import logging
import glob
import os
import yaml
import re
from io import StringIO

from rich.tree import Tree
from rich.markup import escape
from rich.table import Table
from rich.console import Console
from rich import print as rprint


# Set logging to timestamped entries to stderr
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')



class TColr:
    def __init__(self, arguments):
        self.args = self.__class__.defaults()
        self.args.update(arguments)
        numeric_level = getattr(logging, self.args['log_level'].upper(), None)
        logging.basicConfig(stream=sys.stderr, level=numeric_level)
        logging.getLogger().setLevel(numeric_level)

    @classmethod
    def defaults(cls):
        default_keys = {
            'log_level': 'error',
            'config': 'config.yaml',
        }
        return default_keys



    @classmethod
    def setup_args(cls, arguments):
        parser = ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            exit_on_error=False,
            description='''

Color the tabular output based on the given config file


'''
        )
        defaults = cls.defaults()
        parser.set_defaults(**(cls.defaults()))
        parser.add_argument('--log-level', help="Logging level", default=defaults['log_level'])
        parser.add_argument('--input', '-i', help="Input file")
        _args = vars(parser.parse_args(arguments))
        return _args

    def to_ansi(self, text, style):
        tmp_console = Console(file=None, highlight=False, color_system='standard')
        retval = None
        with tmp_console.capture() as capture:
            tmp_console.print(text, style=style, soft_wrap=True, end='')
        retval = capture.get()
        return retval

    def generate_columns(self, header):
        columns = []
        for col in re.findall(r'(\S+\s+)', header):
            columns.append({'name': col.strip(), 'length': len(col)})
        match = re.search(r'(\S+)$', header)
        if match:
            columns.append({'name': match.group(1), 'length': 9999 })
        logging.debug(columns)
        return columns

    def generate_values_from_columns(self, line, columns):
        values = {}
        for col in columns:
            values[col['name']] = line[:col['length']]
            line = line[col['length']:]
        return values

    def is_match(self, value, match):
        # compare based on regex match
        if re.match(match, value):
            return True
        return False

    def apply_color_rules(self, values):
        for rule in self.config.get('rules', []):
            column = rule['column']
            match = rule['match']
            color = rule['color']
            logging.info(f'Testing color rule: {rule} to {values[column]}')
            if column in values and self.is_match(values[column], match):
                logging.info(f'Applying color rule: {rule} to {values[column]}')
                values[column] = self.to_ansi(values[column], color)
        return values

    def print_line(self, values, columns):
        line = ''
        for col in columns:
            if col['length'] == 9999:
                line += values[col['name']]
            else:
                line += values[col['name']].ljust(col['length'])
        logging.debug('[O] ' + line)
        print(line.strip())


    def process_line(self, line, columns):
        logging.debug('[I] ' + line)

        values = self.generate_values_from_columns(line, columns)
        logging.debug(values)
        colored_values = self.apply_color_rules(values)
        logging.debug(colored_values)
        self.print_line(colored_values, columns)


    def process_stream(self, stream):
        # read first line from stream for processing into headers
        header = stream.readline().strip()
        columns = self.generate_columns(header)
        logging.debug('[H] ' + header)
        print(header)
        for line in stream:
            self.process_line(line, columns)

    def run(self, overrides=None):
        if overrides:
            self.args.update(overrides)
        # open the config file
        with open(self.args['config'], 'r') as f:
            self.config = yaml.safe_load(f)
        logging.debug(self.config)

        # Read from input file or stdin
        if self.args['input']:
            with open(self.args['input'], 'r') as f:
                self.process_stream(f)
        else:
            self.process_stream(sys.stdin)


def main(sys_args=None):
    try:
        if sys_args is None:
            sys_args = sys.argv
        args = TColr.setup_args(sys_args[1:])
        cli = TColr(args)
        return cli.run()
    except RuntimeError as e:
        logging.error(str(e))
        return 1
    except SystemExit as ex:
        logging.error(str(ex))
        return 3
    except Exception as e:
        # Unexpected error - show full stack trace
        logging.exception(str(e))
        return 2


if __name__ == '__main__':
    sys.exit(main())
