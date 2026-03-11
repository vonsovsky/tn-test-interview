import logging
import time

from tn_test_interview.client_IO import Operator, OperatorEnum

logger = logging.getLogger(__name__)

class Calculator:
    def perform_operation(self, numbers: list, operator: Operator):
        time.sleep(3)
        logger.info(f"Performing operation: {operator.type.value} on numbers: {numbers}")
        if operator.requires_extra_param:
            logger.debug(f"Extra parameter: {operator.extra_param}")

        try:
            if operator.type == OperatorEnum.SUM:
                result = sum(numbers)
                logger.debug(f"Sum operation: {numbers} = {result}")
                return result
            elif operator.type == OperatorEnum.MULTIPLY:
                result = numbers[0] if numbers else 1
                for num in numbers[1:]:
                    result *= num
                logger.debug(f"Multiply operation: {numbers} = {result}")
                return result
            elif operator.type == OperatorEnum.ADD :
                if operator.requires_extra_param and operator.extra_param is not None:
                    new_list = [number + operator.extra_param for number in numbers]
                    logger.debug(f"Add operation: {numbers} + {operator.extra_param} = {new_list}")
                    return new_list
                else:
                    raise ValueError("Operator 'add' requires an extra parameter.")
            elif operator.type == OperatorEnum.MULTIPLY_BY:
                if operator.requires_extra_param and operator.extra_param is not None:
                    new_list = [number * operator.extra_param for number in numbers]
                    logger.debug(f"MultiplyBy operation: {numbers} * {operator.extra_param} = {new_list}")
                    return new_list
                else:
                    raise ValueError("Operator 'multiply_by' requires an extra parameter.")
            elif operator.type == OperatorEnum.SEND_FIRST:
                if len(numbers) == 0:
                    return []
                result = [numbers[0]] * len(numbers)
                logger.debug(f"SendFirst operation: {numbers} = {result}")
                return result
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        except Exception as e:
            logger.error(f"Error during {operator.type.value} operation: {e}")
            raise
