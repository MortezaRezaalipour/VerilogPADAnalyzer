import sys
import os
from src.arguments import Arguments
from src.synthesis import Synthesis


def VerilogPAD():
    # take in teh cli arguments
    args = Arguments.parse()
    # create a temporary directory for the intermediate files
    os.makedirs(f'{sys.argv[0]}.temp', exist_ok=True)
    os.makedirs(f'{sys.argv[0]}.report', exist_ok=True)

    # To use as a main module
    syn_obj = Synthesis(args.input_path, f'{sys.argv[0]}.temp', f'{sys.argv[0]}.report')

    # To use as an external library
    Synthesis.area(args.input_path, f'{sys.argv[0]}.temp', f'{sys.argv[0]}.report')
    Synthesis.delay(args.input_path, f'{sys.argv[0]}.temp', f'{sys.argv[0]}.report')
    Synthesis.power(args.input_path, f'{sys.argv[0]}.temp', f'{sys.argv[0]}.report')


if __name__ == "__main__":
    VerilogPAD()
