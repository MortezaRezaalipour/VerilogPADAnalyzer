from typing import List
import argparse

class Arguments:
    def __init__(self, tmp_args: argparse):
        self._input_path = tmp_args.input_path

    @property
    def input_path(self):
        return self._input_path


    @classmethod
    def parse(cls) :
        my_parser = argparse.ArgumentParser(description='Verilog Power-Area-Delay Analyzer',
                                            usage='%(prog)s path-to-benchmark')

        my_parser.add_argument('input_path',
                               type=str,
                               default=None,
                               help='benchmark-name')


        tmp_args = my_parser.parse_args()

        return Arguments(tmp_args)

    def __repr__(self):
        return f'An object of class Arguments:\n' \
               f'{self._input_path = }\n'

