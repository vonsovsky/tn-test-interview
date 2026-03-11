
from tn_test_interview.client_IO import OperatorEnum
import pytest

from .utils.program_api import ProgramAPI
"""
ProgramAPI is a helper class to run the program and send inputs to it. It also captures the output for verification.
For runnig program:
api = ProgramAPI()
api.run_program()

For sending input
api.send_input(numbers=[1, 2], operator=OperatorEnum.SUM)

For getting output
output = api.get_output()
"""


@pytest.mark.parametrize("numbers, operator, ap, expected_output", [
                         ([1, 2], OperatorEnum.SUM, None, "3")]
                         )
def test_basic_path(numbers, operator, ap, expected_output):
    """Test the basic path of the program with simple addition"""
    api = ProgramAPI()
    api.run_program()
    api.send_input(numbers=numbers, operator=operator, additional_parameter=ap)
    output = api.get_output()
    assert output == expected_output
    api.stop()
