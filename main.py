from calculator import Calculator
from decimal import Decimal, InvalidOperation

class AddCommand:
    def execute(self, a, b):
        return a + b

class SubtractCommand:
    def execute(self, a, b):
        return a - b

class MultiplyCommand:
    def execute(self, a, b):
        return a * b

class DivideCommand:
    def execute(self, a, b):
        if b != 0:
            return a / b
        else:
            raise ZeroDivisionError("Error: Division by zero.")

from calculator import Calculator
from decimal import Decimal, InvalidOperation

def main():
    calculator = Calculator()

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

                # Dynamically call the corresponding method based on user input
                if command == 'add':
                    result = calculator.add(a_decimal, b_decimal)
                elif command == 'subtract':
                    result = calculator.subtract(a_decimal, b_decimal)
                elif command == 'multiply':
                    result = calculator.multiply(a_decimal, b_decimal)
                elif command == 'divide':
                    result = calculator.divide(a_decimal, b_decimal)

                print(f"The result is: {result}")

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
