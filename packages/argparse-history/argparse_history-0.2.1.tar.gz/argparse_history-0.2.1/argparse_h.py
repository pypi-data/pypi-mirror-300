import argparse
import json
from datetime import datetime
import os
import sys


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        self.default_history_file = kwargs.pop('history_file', 'command_history.json')
        super().__init__(*args, **kwargs)
        self._parsed_args = None

        script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        self.default_history_file = f"{script_name}_{self.default_history_file}"

        # Add the show-history, show-stats, history-dir, and show-args arguments
        self.add_argument('--show-history', action='store_true', help='Show command history')
        self.add_argument('--show-stats', action='store_true', help='Show command history and execution statistics')
        self.add_argument('--history-dir', default='.', help='Directory to store the history file')
        self.add_argument('--show-args', metavar='TIMESTAMP', help='Show arguments for a specific timestamp')
        self._can_update = False

    def parse_args(self, *args, **kwargs):
        # First, parse only the --show-history, --show-stats, --history-dir, and --show-args arguments
        preparser = argparse.ArgumentParser(add_help=False)
        preparser.add_argument('--show-history', action='store_true')
        preparser.add_argument('--show-stats', action='store_true')
        preparser.add_argument('--history-dir', default='.')
        preparser.add_argument('--show-args')
        preargs, remaining_args = preparser.parse_known_args()

        # Set the history file path
        self.history_file = os.path.join(preargs.history_dir, self.default_history_file)

        if preargs.show_history:
            # If --show-history is provided, show the history and exit
            self.show_history()
            sys.exit(0)

        if preargs.show_stats:
            self.show_stats()
            sys.exit(0)

        if preargs.show_args:
            self.show_args(preargs.show_args)
            sys.exit(0)

        # If --show-history, --show-stats, and --show-args are not provided, parse all arguments as usual
        parsed_args = super().parse_args(remaining_args, *args, **kwargs)
        self._record_history(parsed_args)
        self._can_update = True
        self._parsed_args = parsed_args
        return parsed_args

    def _record_history(self, args):
        history = self._load_history()
        args_dict = vars(args)
        # Remove 'show_history' and 'history_dir' from the arguments to be recorded
        args_dict.pop('show_history', None)
        args_dict.pop('show_stats', None)
        args_dict.pop('show_args', None)
        args_dict.pop('history_dir', None)
        timestamp = datetime.now().replace(microsecond=0).isoformat()
        history.append({
            'timestamp': timestamp,
            'arguments': args_dict
        })
        self._save_history(history)

    def _load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_history(self, history):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def show_history(self):
        history = self._load_history()
        for entry in history:
            print(f"Timestamp: {entry['timestamp']}")
            print("Arguments:")
            for arg, value in entry['arguments'].items():
                print(f"  {arg}: {value}")
            print()

    def show_stats(self):
        history = self._load_history()
        for entry in history:
            print(f"Timestamp: {entry['timestamp']}")
            print("Arguments:")
            for arg, value in entry['arguments'].items():
                print(f"  {arg}: {value}")
            print("Statistics:")
            if not ('stats' in entry):
                print(f'  No statistics recorded')
                continue
            for arg, value in entry['stats'].items():
                print(f"  {arg}: {value}")
            print()

    def show_args(self, timestamp):
        history = self._load_history()
        for entry in history:
            if entry['timestamp'] == timestamp:
                args = []
                for arg, value in entry['arguments'].items():
                    if isinstance(value, bool):
                        if value:
                            args.append(f"--{arg}")
                    elif isinstance(value, (int, float, str)):
                        args.append(f"--{arg} {value}")
                    elif isinstance(value, list):
                        for item in value:
                            args.append(f"--{arg} {item}")
                print(" ".join(args))
                return
        print(f"No entry found for timestamp: {timestamp}")

    def print_args(self):
        if self._parsed_args is None:
            print("Error: Arguments have not been parsed yet. Call parse_args() first.")
            return
        print("Parsed arguments:")
        for arg, value in vars(self._parsed_args).items():
            print(f"  {arg}: {value}")

    def add_data(self, new_data):
        if not self._can_update:
            print(f"Error: arguments have not yet been parsed! Call `parse_args()` first!")
            return

        json_file = self.history_file
        # Check if the file exists
        if not os.path.exists(json_file):
            print(f"Error: File {json_file} does not exist! Has it been deleted?")
            return

        # Read the existing JSON data
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Ensure the data is a list and not empty
        if not isinstance(data, list) or len(data) == 0:
            print(f"Error: history file {json_file} does not contain a list of records or is empty.")
            return

        # Update the last record
        data[-1].update({"stats": new_data})

        # Write the updated data back to the file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)
