# Test suite that runs main.py and sends all inputs from input_output.csv
import pytest
import csv
import sys
import subprocess
from pathlib import Path


def load_test_cases():
    """Load all test cases from input_output.csv"""
    test_cases = []
    csv_path = Path(__file__).parent / 'input_output.csv'

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append((row['input'], row['expected_output']))

    return test_cases


@pytest.mark.parametrize("input_str,expected_output", load_test_cases(),
                         ids=[f"test_{i}" for i in range(len(load_test_cases()))])
def test_main_program(input_str, expected_output):
    """Send each input to main.py and verify the output"""
    main_py = Path(__file__).parent.parent / 'src' / 'main.py'

    # Run main.py with the input
    result = subprocess.run(
        [sys.executable, str(main_py)],
        input=f"{input_str}\nexit\n",
        capture_output=True,
        text=True,
        timeout=10
    )

    # Extract the answer from output (format: "A: <result>")
    for line in result.stdout.split('\n'):
        if line.startswith("A:"):
            actual_output = line.replace("A:", "").strip()
            print("=====================")
            print(actual_output)
            assert actual_output == expected_output, \
                f"Input: {input_str}\nExpected: {expected_output}\nGot: {actual_output}"
            return

    # If no answer found, test fails
    pytest.fail(f"No answer found for input: {input_str}\nOutput:\n{result.stdout}")

