from setuptools import setup, find_packages
import os


VERSION = '0.0.1'
DESCRIPTION = """
VerilogPADAnalyzer is a Python application designed to analyze and report the
Power, Area, and Delay (PAD) of Verilog input circuits.
"""


# Setting up
setup(
    name="verilog-pad-analyzer",
    version=VERSION,
    author="Morteza Rezaalipour (MorellRAP)",
    author_email="<rezaalipour.usi@gmail.com>",
    description='A library for Power, Area, and Delay analysis',
    long_description=DESCRIPTION,
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
