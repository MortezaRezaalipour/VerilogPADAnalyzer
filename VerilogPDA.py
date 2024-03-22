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
    syn_obj = Synthesis(args.input_path, f'{sys.argv[0]}.temp', f'{sys.argv[0]}.report')



if __name__ == "__main__":
    VerilogPAD()
