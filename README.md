# VerilogPADAnalyzer

VerilogPAD is Python tool designed to analyze Verilog files, providing power, area, and delay metrics.
It is also released as a PyPi package under the name `verilog-pad-analyzer` (https://pypi.org/project/verilog-pad-analyzer/). 

You may simply import it into your Python project by installing this package witht the command 

```bash 
$ pip install verilog-pad-analyzer
```


## Prerequisits
- Install the following tools:
1. **Python**
2. **Linux**
3. **Yosys**: link (https://github.com/YosysHQ/yosys)
4. **OpenSTA**: link (https://github.com/The-OpenROAD-Project/OpenSTA)
5. **Icarus Verilog**: link (https://github.com/steveicarus/iverilog)

**Note: add the binaries of 3, 4, and 5 to your PATH**

## Features
- **Comprehensive Analysis**: Compute detailed metrics for power consumption, physical area, and timing delay of Verilog circuits.
- **Intermediate File Handling**: Automatically manages intermediate files in a temporary directory to keep the workspace clean.
- **Report Generation**: Outputs analysis results in separate, organized report files for each metric.


## Folder Structure
- `./config/`: contains the technology library and synthesizer scripts
- `./src/`: contains the main classes and modules of the project
- `./VerilogPDA.py.temp/`: a temporary folder that is automatically created and stores the intermediate files such as synthesized files (can be safely removed afterward).
- `./VerilogPDA.py.report/`: a temporary folder that is automatically created and stores the area, power, and delay reports (can be safely removed afterward).

## Usage

To run the VerilogPADAnalyzer, use the following syntax:



### Arguments

```
$ python3 VerilogPDA.py [path-to-input]
```
For example, assuming that a circuit called `abs_diff_i4_o3.v` is located at the root directory, one can get the area, power, and delay reports of this circuit using the following command: 

```
$ python3 VerilogPDA.py abs_diff_i4_o3.v
```
Upon launching the command above, three report files will be generated in `./VerilogPDA.py.report/` directory. 


## Contributing
Contributions to the project are welcome. Please follow the standard GitHub pull request process to propose changes.


## Contact
For any inquiries or contributions, please contact Morteza at Rezaalipour.usi@gmail.com.
