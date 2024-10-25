import multiprocessing
import sys
import importlib
import os
from decimal import Decimal, InvalidOperation
from collections import OrderedDict
import logging
import logging.config
import pandas as pd
from dotenv import load_dotenv
from app.Calculations import Calculations
from app.Calculation import Calculation

# Load environment variables
def load_environment_variables():
    load_dotenv()
    settings = {key: value for key, value in os.environ.items()}
    logging.info("Environment variables loaded.")
    
    # Check for necessary environment variables
    required_vars = ['ENVIRONMENT']
    for var in required_vars:
        if var not in settings:
            logging.warning(f"Environment variable {var} is not set.")
    return settings

# Configure logging
def configure_logging():
    os.makedirs("logs", exist_ok=True)
    logging_conf_path = "logging.conf"
    if os.path.exists(logging_conf_path):
        logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
    else:
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    logging.info("Logging configured.")

# Load plugins dynamically
def load_plugins():
    commands = OrderedDict()
    plugins_dir = os.path.join('app', 'plugins')
    
    if not os.path.exists(plugins_dir):
        logging.warning(f"Plugins directory not found: {plugins_dir}")
        return commands
    
    for filename in os.listdir(plugins_dir):
        if filename.endswith('_command.py'):
            try:
                module_name = filename[:-3]  
                module = importlib.import_module(f'app.plugins.{module_name}')
                command_class = getattr(module, module_name[:-8].capitalize() + 'Command')
                commands[module_name[:-8]] = command_class()
                logging.info(f"Loaded plugin: {module_name}")
            except (ImportError, AttributeError) as e:
                logging.error(f"Failed to load plugin {module_name}: {e}")

    return commands

# Decorator for logging execution
def log_execution(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

@log_execution
def perform_calculation_and_display(num1, num2, operation_type, commands, use_multiprocessing=False):
    """
    Performs the specified arithmetic operation on two numbers.
    """
    try:
        decimal_num1, decimal_num2 = map(Decimal, [num1, num2])
        operation_function = commands.get(operation_type)
        if not operation_function:
            print(f"Unknown operation: {operation_type}")
            return
        
        # Perform the calculation, either using multiprocessing or not
        if use_multiprocessing:
            result_queue = multiprocessing.Queue()
            try:
                process = multiprocessing.Process(
                    target=operation_function.execute_multiprocessing,
                    args=(decimal_num1, decimal_num2, result_queue)
                )
                process.start()
                process.join()
                result = result_queue.get()
                print(f"The result of {num1} {operation_type} {num2} using multiprocessing is {result}")
            except Exception as e:
                logging.error(f"Multiprocessing failed: {e}")
                print(f"Multiprocessing failed: {e}. Running operation without multiprocessing.")
                result = operation_function.execute(decimal_num1, decimal_num2)
                print(f"The result of {num1} {operation_type} {num2} is {result}")
        else:
            # Use the execute method on the command object
            result = operation_function.execute(decimal_num1, decimal_num2)
            print(f"The result of {num1} {operation_type} {num2} is {result}")

        # Create a Calculation instance
        calculation = Calculation(decimal_num1, decimal_num2, operation_function)
        # Perform the calculation using the operate method
        calculation_result = calculation.operate()
        print(f"Calculation result stored: {calculation_result}")

        # Add the calculation to the history
        Calculations.add_calculation(calculation)

    except InvalidOperation:
        logging.error(f"Invalid number input: {num1} or {num2} is not a valid number.")
        print(f"Invalid number input: {num1} or {num2} is not a valid number.")
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An error occurred: {e}")

# Run the REPL interface
@log_execution
def run_repl(commands):
    """
    Run the REPL (Read-Eval-Print Loop) for interactive calculations.
    """
    print("Entering REPL mode. Type 'exit' to quit.")
    print("Add 'mp' at the end of a command to use multiprocessing.")
    
    while True:
        user_input = input("Enter command: ")
        if user_input == 'exit':
            print("Exiting REPL mode...")
            break
        elif user_input == 'menu':
            print("Available Commands:")
            for cmd_name in commands:
                print(f"- {cmd_name}")
            continue
        elif user_input == 'history':
            history_df = Calculations.get_all_calculations()
            if history_df.empty:
                print("No calculations in history.")
            else:
                print(history_df)
            continue
        elif user_input == 'clear_history':
            Calculations.clear_history()
            print("History cleared.")
            continue
        elif user_input.startswith('save_history'):
            _, filepath = user_input.split(maxsplit=1)
            Calculations.save_history(filepath)
            print(f"History saved to {filepath}.")
            continue
        elif user_input.startswith('load_history'):
            _, filepath = user_input.split(maxsplit=1)
            if os.path.exists(filepath):
                Calculations.load_history(filepath)
                print(f"History loaded from {filepath}.")
            else:
                print(f"File not found: {filepath}")
            continue
        elif user_input == 'latest':
            # Display the latest calculation
            latest_calculation = Calculations.get_latest()
            if latest_calculation:
                print(f"Latest calculation: {latest_calculation}")
            else:
                print("No calculations in history.")
            continue
        elif user_input.startswith('delete_history'):
            try:
                _, index_str = user_input.split(maxsplit=1)
                index = int(index_str)
                Calculations.delete_history(index)
            except (ValueError, IndexError):
                print("Usage: delete_history <index>")
            continue
        elif user_input.startswith('filter_with_operation'):
            try:
                _, operation_name = user_input.split(maxsplit=1)
                filtered_df = Calculations.filter_with_operation(operation_name)
                if filtered_df.empty:
                    print(f"No calculations found for operation: {operation_name}")
                else:
                    print(filtered_df)
            except ValueError:
                print("Usage: filter_with_operation <operation_name>")
            continue

        # Handling arithmetic commands
        parts = user_input.split()
        if len(parts) not in [3, 4]:  
            print("Usage: <command> <num1> <num2> [mp]")
            continue

        command_name, num1, num2 = parts[:3]
        use_multiprocessing = len(parts) == 4 and parts[3] == 'mp'

        if command_name not in commands:
            print(f"Unknown command: {command_name}")
            continue

        perform_calculation_and_display(num1, num2, command_name, commands, use_multiprocessing)



# Main function
@log_execution
def main():
    """
    Main function to handle command-line arguments and initiate the calculation.
    """
    commands = load_plugins()  

    if len(sys.argv) == 4:  
        _, num1, num2, operation_type = sys.argv
        perform_calculation_and_display(num1, num2, operation_type, commands)
        
    elif len(sys.argv) == 5:  
        _, num1, num2, operation_type, mp_flag = sys.argv
        use_multiprocessing = mp_flag == "mp"
        perform_calculation_and_display(num1, num2, operation_type, commands, use_multiprocessing)
    
    elif len(sys.argv) == 2 and sys.argv[1] == 'repl':  
        run_repl(commands)
        
    else:
        print("Usage: python main.py <number1> <number2> <operation> [mp] or python main.py repl")

# Entry point
if __name__ == '__main__':
    configure_logging()
    settings = load_environment_variables()
    logging.info(f"Environment: {settings.get('ENVIRONMENT')}")
    logging.info("Application started.")
    main()
