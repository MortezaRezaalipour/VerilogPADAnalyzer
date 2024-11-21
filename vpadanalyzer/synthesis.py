import re
import subprocess
from subprocess import PIPE
import os
from . import config
from .paths import OPENSTA, YOSYS

class Synthesis:
    def __init__(self, input_path: str, temp_dir: str = None, report_dir: str = None):
        self._input_path = input_path
        self._module_name = self.__get_module_name()
        self._temp_dir = f'{temp_dir}' if temp_dir else 'temp'
        self._rep_dir = f'{report_dir}' if report_dir else 'report'
        os.makedirs(self._temp_dir, exist_ok=True)
        os.makedirs(self._rep_dir, exist_ok=True)
        self._syn_path = f'{self._temp_dir}/{self._module_name}_syn.v'
        self._power_script = f'{self._temp_dir}/{self._module_name}_power.script'
        self._delay_script = f'{self._temp_dir}/{self._module_name}_delay.script'

        self._area = None
        self._power = None
        self._delay = None

        self._config_path = self.get_config_path()
        self._lib_path = f'{self._config_path}/gscl45nm.lib'
        self._abc_script_path = f'{self._config_path}/abc.script'


    # =========================

    def get_config_path(self):
        init_address = os.path.abspath(config.__file__)
        init_address = init_address.replace('__init__.py', "")
        return init_address
    def get_area(self) -> float:
        """
        measures the area with yosys synthesis tool with the tech. library specified
        :return: a float number representing the area
        """
        yosys_command = f"read_verilog \"{self._input_path}\";\n" \
                        f"synth -flatten;\n" \
                        f"opt;\n" \
                        f"opt_clean -purge;\n" \
                        f"abc -liberty {self._lib_path} -script {self._abc_script_path};\n" \
                        f"stat -liberty {self._lib_path};\n"

        process = subprocess.run([YOSYS, '-p', yosys_command], stdout=PIPE, stderr=PIPE)
        if process.stderr:
            raise Exception(f'Yosys ERROR!!!\n {process.stderr.decode()}')
        else:

            if re.search(r'Chip area for .*: (\d+.\d+)', process.stdout.decode()):
                area = re.search(r'Chip area for .*: (\d+.\d+)', process.stdout.decode()).group(1)

            elif re.search(r"Don't call ABC as there is nothing to map", process.stdout.decode()):
                area = 0
            else:
                raise Exception('Yosys ERROR!!!\nNo useful information in the stats log!')


        with open(f'{self._rep_dir}/{self._module_name}.area', 'w') as a:
            a.write(f'{float(area)}\n')
            self._area = float(area)
        return float(area)

    def get_power(self):
        """
        measures the power with opensta synthesis tool with the tech. library specified
        :return: a float number representing the power
        """
        self.__synthesize()

        sta_command = f"read_liberty {self._lib_path}\n" \
                      f"read_verilog {self._syn_path}\n" \
                      f"link_design {self._module_name}\n" \
                      f"create_clock -name clk -period 1\n" \
                      f"set_input_delay -clock clk 0 [all_inputs]\n" \
                      f"set_output_delay -clock clk 0 [all_outputs]\n" \
                      f"report_checks\n" \
                      f"report_power -digits 12\n" \
                      f"exit"

        with open(self._power_script, 'w') as ds:
            ds.writelines(sta_command)
        # process = subprocess.run([sxpatconfig.OPENSTA, power_script], stderr=PIPE)

        process = subprocess.run([OPENSTA, self._power_script], stdout=PIPE, stderr=PIPE)
        if process.stderr:
            raise Exception(f'OpenSTA ERROR!!!\n {process.stderr.decode()}')
        else:
            os.remove(self._power_script)
            pattern = r"Total\s+(\d+.\d+)[^0-9]*\d+\s+(\d+.\d+)[^0-9]*\d+\s+(\d+.\d+)[^0-9]*\d+\s+(\d+.\d+[^0-9]*\d+)\s+"
            if re.search(pattern, process.stdout.decode()):
                total_power_str = re.search(pattern, process.stdout.decode()).group(4)

                if re.search(r'e[^0-9]*(\d+)', total_power_str):
                    total_power = float(re.search(r'(\d+.\d+)e[^0-9]*\d+', total_power_str).group(1))
                    sign = (re.search(r'e([^0-9]*)(\d+)', total_power_str).group(1))
                    if sign == '-':
                        sign = -1
                    else:
                        sign = +1
                    exponent = int(re.search(r'e([^0-9]*)(\d+)', total_power_str).group(2))
                    total_power = total_power * (10 ** (sign * exponent))
                else:
                    total_power = total_power_str

                with open(f'{self._rep_dir}/{self._module_name}.power', 'w') as a:
                    a.write(f'{float(total_power)}\n')

                self._power = float(total_power)
                return float(total_power)

            else:
                print('OpenSTA Warning! Design has 0 power consumption!')
                with open(f'{self._rep_dir}/{self._module_name}.power', 'w') as a:
                    a.write(f'{float(0)}\n')
                self._power = float(0)
                return 0


    def get_delay(self):
        """
        measures the delay with opensta synthesis tool with the tech. library specified
        :return: a float number representing the delay
        """
        self.__synthesize()

        sta_command = f"read_liberty {self._lib_path}\n" \
                      f"read_verilog {self._syn_path}\n" \
                      f"link_design {self._module_name}\n" \
                      f"create_clock -name clk -period 1\n" \
                      f"set_input_delay -clock clk 0 [all_inputs]\n" \
                      f"set_output_delay -clock clk 0 [all_outputs]\n" \
                      f"report_checks -digits 6\n" \
                      f"exit"
        with open(self._delay_script, 'w') as ds:
            ds.writelines(sta_command)
        # process = subprocess.run([sxpatconfig.OPENSTA, delay_script], stderr=PIPE)
        process = subprocess.run([OPENSTA, self._delay_script], stdout=PIPE, stderr=PIPE)
        if process.stderr:
            raise Exception(f'Yosys ERROR!!!\n {process.stderr.decode()}')
        else:
            os.remove(self._delay_script)
            if re.search('(\d+.\d+).*data arrival time', process.stdout.decode()):
                time = re.search('(\d+.\d+).*data arrival time', process.stdout.decode()).group(1)
                with open(f'{self._rep_dir}/{self._module_name}.delay', 'w') as a:
                    a.write(f'{float(time)}\n')
                self._delay = float(time)
                return float(time)
            else:
                print('OpenSTA Warning! Design has 0 delay!')
                with open(f'{self._rep_dir}/{self._module_name}.delay', 'w') as a:
                    a.write(f'{float(0)}\n')
                self._delay = float(0)
                return 0


    def __synthesize(self):
        """
        reads the Verilog file located by self._input_path property and synthesizes it into gate level according to
        tech. library located at "DEFAULT_LIB" and according to the script located at "ABC_SCRIPT_PATH" and dumps the
        synthesized netlist onto "self._syn_path"
        :return: nothing
        """

        yosys_command = f"read_verilog {self._input_path};\n" \
                        f"synth -flatten;\n" \
                        f"opt;\n" \
                        f"opt_clean -purge;\n" \
                        f"abc -liberty {self._lib_path} -script {self._abc_script_path};\n" \
                        f"write_verilog -noattr {self._syn_path}"
        process = subprocess.run([YOSYS, '-p', yosys_command], stdout=PIPE, stderr=PIPE)
        if process.stderr:
            raise Exception(f'Yosys ERROR!!!\n {process.stderr.decode()}')

    def __get_module_name(self):
        """
        reads the Verilog file located at "self._input_path", parses the module signature and extract the module's name
        Example:
        imaging the module signature of a Verilog file is as such:

        module adder_i4_o3(i0, i1, i2, i3, o0, o1, o2);
        ... the rest of the code
        endmodule;

        in this case, this function returns "adder_i4_o3"
        :return: a str that contains the module's name
        """
        with open(self._input_path, 'r') as dp:
            contents = dp.readlines()
            for line in contents:
                if re.search(r'module\s+(.*)\(', line):
                    modulename = re.search(r'module\s+(.*)\(', line).group(1)
        modulename = modulename.strip()
        return modulename

    # =========================
    """
    For use as a PyPI package
    """
    @classmethod
    def area(cls, input_path: str, temp_dir: str = None, report_dir: str = None):
        """
        measures the area with yosys synthesis tool with the tech. library specified
        :return: a float number representing the area
        """
        synth_obj = Synthesis(input_path, temp_dir, report_dir)
        synth_obj._area = synth_obj.get_area()
        return synth_obj._area
    @classmethod
    def power(cls, input_path: str, temp_dir: str = None, report_dir: str = None):
        """
        measures the power with opensta synthesis tool with the tech. library specified
        :return: a float number representing the power
        """
        synth_obj = Synthesis(input_path, temp_dir, report_dir)
        synth_obj._power = synth_obj.get_power()
        return synth_obj._power

    @classmethod
    def delay(cls, input_path: str, temp_dir: str = None, report_dir: str = None):
        """
        measures the delay with opensta synthesis tool with the tech. library specified
        :return: a float number representing the delay
        """
        synth_obj = Synthesis(input_path, temp_dir, report_dir)
        synth_obj._delay = synth_obj.get_delay()
        return  synth_obj._delay
    # =========================

    def __repr__(self):
        return f'An object of class Synthesis:\n' \
            f'{self._module_name = }\n' \
            f'{self._input_path = }\n' \
            f'{self._area = }\n' \
            f'{self._power = }\n' \
            f'{self._delay = }\n'


