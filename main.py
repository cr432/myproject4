from decimal import Decimal, InvalidOperation
from calculator import Calculator
from plugins.plugin_interface import CommandPlugin
from importlib import import_module
import os
import inspect
from multiprocessing import Process, Manager

def load_plugins():
    plugins = []

    # Load plugins from the 'plugins' directory
    plugins_directory = os.path.join(os.path.dirname(__file__), 'plugins')
    for file_name in os.listdir(plugins_directory):
        if file_name.endswith('_plugin.py'):
            module_name = file_name[:-3]  # Remove '.py' extension
            module = import_module(f'plugins.{module_name}')
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, CommandPlugin) and obj != CommandPlugin:
                    plugins.append(obj())

    return plugins

def execute_command(plugin, a, b, results):
    try:
        result = plugin.execute(a, b)
        results[plugin.__class__.__name__.lower()] = result
    except Exception as e:
        results[plugin.__class__.__name__.lower()] = str(e)

def main():
    calculator = Calculator()
    plugins = load_plugins()

    while True:
        command = input("Enter command (add/subtract/multiply/divide/menu/exit): ").lower()

        if command == 'exit':
            break

        if command == 'menu':
            calculator.menu(0, 0)  # Call the menu command with dummy operands

        elif command in ['add', 'subtract', 'multiply', 'divide']:
            a = input("Enter first number: ")
            b = input("Enter second number: ")

            try:
                a_decimal, b_decimal = map(Decimal, [a, b])

                # Dynamically call the corresponding plugin based on user input
                for plugin in plugins:
                    if command == plugin.__class__.__name__.lower():
                        results = Manager().dict()
                        processes = []

                        for plugin in plugins:
                            p = Process(target=execute_command, args=(plugin, a_decimal, b_decimal, results))
                            processes.append(p)
                            p.start()

                        for p in processes:
                            p.join()

                        for plugin_name, result in results.items():
                            print(f"The result of {plugin_name} is: {result}")

                        break
                else:
                    print(f"Unknown command: {command}")

            except InvalidOperation:
                print(f"Invalid number input: {a} or {b} is not a valid number.")
            except ZeroDivisionError as e:
                print(str(e))
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
        else:
            print("Unknown command. Please enter a valid command.")

if __name__ == '__main__':
    main()
