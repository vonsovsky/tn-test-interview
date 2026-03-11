import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class OperatorEnum(Enum):
    SUM = 'sum'
    ADD = 'add'
    MULTIPLY = 'multiply'
    MULTIPLY_BY = 'multiply_by'
    SEND_FIRST = 'send_first'

def parse_number(value: str) -> int | float:
    try:
        if '.' not in value:
            return int(value)
        else:
            return float(value)
    except ValueError:
        # BUG: Silent fail - float() may raise ValueError for truly invalid input like "abc"
        return float(value)

@dataclass
class Operator:
    type: OperatorEnum
    requires_extra_param: bool = False
    extra_param: int | float = None

class ClientIO:
    def __init__(self) -> None:
        self.input: str = ""
        self.numbers: list = []
        self.operator: str = ""

    def get_input(self) -> str:
        """Get input from user console"""
        try:
            self.input = input("\nEnter numbers and operator: ").strip()
            logger.info(f"Received input: {self.input}")
            return self.input
        except Exception as e:
            logger.error(f"Error reading input: {e}")
            raise

    def parse_input(self) -> tuple[list, Operator]:
        """
        Parse input to extract numbers and operator
        Expected formats:
        - "1 2 3 sum" -> numbers=[1,2,3], operator='sum' -> numbers=6
        - "1 2 3 4 add 2" -> numbers=[1,2,3,4], operator='add', extra_param=2 -> numbers=[3,4,5,6]
        - "2 4 6 multiply" -> numbers=[2,4,6], operator='multiply' -> numbers=[48]
        - "2 4 6 multiply_by 3" -> numbers=[2,4,6], operator='multiply_by', extra_param=3 -> numbers=[6,12,18]
        - "1 2 3 send_first" -> numbers=[1,2,3], operator='send_first' -> numbers=[1,1,1]
        """
        try:
            parts = self.input.split()

            if len(parts) < 2:
                raise ValueError("Invalid input format. Provide list of numbers and an operator.")

            operator_index = -1
            valid_operators = ['sum', 'add', 'multiply', 'multiply_by', 'send_first']

            # BUG: First match wins - doesn't check if operator appears in wrong position
            for i, part in enumerate(parts):
                if part.lower() in valid_operators:
                    operator_index = i
                    self.operator = part.lower()
                    break

            if operator_index == -1:
                raise ValueError(f"No valid operator found. Valid operators are: {valid_operators}")

            logger.info(f"Extracted operator: {self.operator} at index {operator_index}")


            number_parts = parts[:operator_index]

            if not number_parts:
                raise ValueError("At least one number must be provided before the operator")

            # Parse numbers as int if they are whole numbers, otherwise as float
            self.numbers = [parse_number(x) for x in number_parts]

            # Check if there's an extra parameter after the operator (for 'add' or 'multiply_by')
            if self.operator in ['add', 'multiply_by']:
                if len(parts) <= operator_index + 1:
                    raise ValueError(f"Operator '{self.operator}' requires an extra parameter after the operator")
                # Parse extra_param as int if it's a whole number, otherwise as float
                extra_param = parse_number(parts[operator_index + 1])
                logger.info(f"Parsed numbers: {self.numbers}, operator: {self.operator}, extra param: {extra_param}")
                return self.numbers, Operator(type=OperatorEnum(self.operator), requires_extra_param=True, extra_param=extra_param)
            else:
                if len(parts) > operator_index + 1:
                    logger.warning(f"Extra parameters after operator '{self.operator}' will be ignored")
                logger.info(f"Parsed numbers: {self.numbers}, operator: {self.operator}")
                return self.numbers, Operator(type=OperatorEnum(self.operator), requires_extra_param=False)

        except ValueError as e:
            logger.error(f"Error parsing input: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during parsing: {e}")
            raise

    def print_output(self, output) -> None:
        """Print output in Q&A format"""
        to_print = output
        if isinstance(output, list):
            to_print = " ".join(str(x) for x in output)
        print(f"Q: {self.input}", flush=True)
        print(f"A: {to_print}\n", flush=True)
        logger.debug(f"Output printed: {output}")
