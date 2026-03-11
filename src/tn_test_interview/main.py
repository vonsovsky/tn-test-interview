import sys
import logging
import argparse
import threading
from queue import Queue
from tn_test_interview.client_IO import ClientIO
from tn_test_interview.mock_logic import Calculator


def setup_logging(log_level: str) -> None:
    """Configure logging with specified level"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Calculator application that processes numbers and operators'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level (default: INFO)'
    )
    return parser.parse_args()


logger = logging.getLogger(__name__)


def input_thread(task_queue: Queue, stop_event: threading.Event) -> None:
    """Thread function to read user input and add to queue"""
    logger.info("Input thread started")
    client_io = ClientIO()

    while not stop_event.is_set():
        try:
            client_io.get_input()

            if client_io.input.lower() in ['exit', 'quit']:
                logger.info("Exit command received")
                stop_event.set()
                break

            logger.info(f"Input received: {client_io.input}")
            if task_queue.qsize() > 3:
                logger.warning("Task queue is full. We will not ad this req")
                continue
            # Add the input to the queue
            task_queue.put(client_io.input)
            logger.info(f"Added task to queue. Queue size: {task_queue.qsize()}")

        except EOFError:
            logger.info("No more input available")
            break
        except Exception as e:
            logger.error(f"Error reading input: {e}")
            continue

    logger.info("Input thread stopped")


def process_thread(task_queue: Queue, stop_event: threading.Event) -> None:
    """Thread function to process tasks from the queue"""
    logger.info("Processing thread started")
    client_io = ClientIO()
    calculator = Calculator()
    while_sum = 0

    while not stop_event.is_set() or not task_queue.empty():
        while_sum += 1
        try:
            # Try to get a task from the queue with a timeout
            task_input = task_queue.get(timeout=1)
            logger.info(f"Processing task from queue. Queue size before: {task_queue.qsize()}")

            try:
                # Set the input for parsing
                client_io.input = task_input

                # Parse the input to extract numbers and operator
                numbers, operator = client_io.parse_input()
                logger.debug(f"Parsed input - Numbers: {numbers}, Operator: {operator}")

                # Perform the operation
                result = calculator.perform_operation(numbers, operator)
                logger.debug(f"Operation result: {result}")

                client_io.print_output(result)
                logger.info(f"Task processed successfully")

            except Exception as e:
                logger.error(f"Error processing input '{task_input}': {e}")
                print(f"Q: {task_input}", flush=True)
                print(f"Error: {e}\n", flush=True)

            # Mark task as done
            task_queue.task_done()

        except:
            if stop_event.is_set() and task_queue.empty():
                break
            continue

    logger.info("Processing thread stopped")


def main() -> int:
    # Parse command-line arguments
    args = parse_arguments()

    # Setup logging with specified level
    setup_logging(args.log_level)

    logger.info("Starting calculator application")
    logger.info(f"Log level set to: {args.log_level}")

    # Create a FIFO queue for tasks
    task_queue = Queue()

    # Create a stop event for thread synchronization
    stop_event = threading.Event()

    # Create and start the input thread
    input_th = threading.Thread(target=input_thread, args=(task_queue, stop_event), daemon=False)
    input_th.start()

    # Create and start the processing thread
    process_th = threading.Thread(target=process_thread, args=(task_queue, stop_event), daemon=False)
    process_th.start()

    try:
        # Wait for both threads to complete
        input_th.join()
        process_th.join()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        stop_event.set()
        input_th.join(timeout=2)
        process_th.join(timeout=2)
        print("\nExiting calculator...")

    logger.info("Calculator application ended")
    return 0

if __name__ == '__main__':
    sys.exit(main())
