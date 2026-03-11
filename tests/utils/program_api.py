import subprocess
import sys
from pathlib import Path

from tn_test_interview.client_IO import OperatorEnum


class ProgramAPI:
    def __init__(self):
        """Initialize the ProgramAPI with process and output buffer"""
        self.process = None
        self.output_buffer = []

    def run_program(self) -> None:
        """This function runs the program so we are able to test it."""
        main_py = Path(__file__).parent.parent.parent / 'src' / 'tn_test_interview' / 'main.py'
        self.process = subprocess.Popen(
            [sys.executable, str(main_py)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send_input(self, numbers: list[int|float], operator: OperatorEnum, additional_parameter: int|float = None) -> None:
        """This function sends input to the program and captures the output."""
        if self.process is None:
            raise RuntimeError("Program not running. Call run_program() first.")

        # Build the input string based on the operator type
        input_str = " ".join(str(n) for n in numbers)
        input_str += f" {operator.value}"

        if additional_parameter is not None:
            input_str += f" {additional_parameter}"

        # Send input to the process
        self.process.stdin.write(input_str + "\n")
        self.process.stdin.flush()

    def get_output(self) -> str:
        """This function retrieves the output from the program."""
        if self.process is None:
            raise RuntimeError("Program not running. Call run_program() first.")

        # Read output lines until we get the "A:" line
        output_lines = []
        answer = None

        while answer is None:
            line = self.process.stdout.readline()
            if not line:
                break
            output_lines.append(line.strip())
            if line.startswith("A:"):
                answer = line.replace("A:", "").strip()

        return answer

    def stop(self) -> None:
        """Stop the program process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
