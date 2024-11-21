from setuptools import setup, find_packages

import os


VERSION = '0.0.7'
DESCRIPTION = """
VerilogPADAnalyzer is a Python application designed to analyze and report the
Power, Area, and Delay (PAD) of Verilog input circuits.
"""

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="verilog-pad-analyzer",
    version=VERSION,
    author="Morteza Rezaalipour (MorellRAP)",
    author_email="<rezaalipour.usi@gmail.com>",
    description=DESCRIPTION,
    include_package_data=True,
    package_data={
        'vdapanalyzer': ['config/*'],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = "https://github.com/MortezaRezaalipour/VerilogPADAnalyzer",
    packages=find_packages(),
    install_requires=[''],
    keywords=['python', 'verilog', 'PAD', 'synthesis', 'analysis', 'circuit', 'EDA', 'simulation', 'hardware', 'design'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
