import argparse
import json
import inspect
from beamdust.beamdust import Beamdust

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Beamdust CLI for API management.")
    parser.add_argument('-u', '--username', required=True, help='Email for authentication.')
    parser.add_argument('-p', '--password', required=True, help='Password for authentication.')
    parser.add_argument('-d', '--docs', action='store_true', help='Generate and open API documentation.')
    parser.add_argument('-l', '--list', action='store_true', help='List all available API methods.')
    parser.add_argument('-fh', '--function-help', help='Show help for a specific function.')

    args = parser.parse_args()

    # Opening message
    print("Welcome to the Beamdust CLI! Use this tool to manage your API interactions.")

    # Initialize Beamdust with provided credentials
    beamdust = Beamdust(email=args.username, password=args.password)

    # List available functions if -l flag is set
    if args.list:
        available_functions = beamdust.get_available_functions()
        print("Available API methods:")
        print(json.dumps(available_functions, indent=4))
        return

    # If the docs flag is set, generate and open the documentation
    if args.docs:
        beamdust.generate_documentation()
        print("Documentation generated and opened successfully.") 
        return

    # Show help for a specific function if the function-help flag is provided
    if args.function_help:
        try:
            method = getattr(beamdust, args.function_help)
            docstring = inspect.getdoc(method)
            print(f"\nDocstring of '{args.function_help}':\n{docstring}\n")
            print(f"Body example: \n")
            print(json.dumps(method(_help=True),indent=4))
        except AttributeError:
            print(f"Error: The function '{args.function_help}' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return  # Exit after displaying the docstring

    print("Available commands:")
    print("  -u, --username      : Email for authentication.")
    print("  -p, --password      : Password for authentication.")
    print("  -d, --docs          : Generate and open API documentation.")
    print("  -l, --list          : List all available API methods.")
    print("  -fh, --function-help: Show help for a specific function.")


if __name__ == "__main__":
    main()
