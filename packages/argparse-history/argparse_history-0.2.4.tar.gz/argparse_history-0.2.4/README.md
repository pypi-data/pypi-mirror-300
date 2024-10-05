# argparse-history

## Why Track Command History?

Have you ever found yourself wondering:
- "What parameters did I use for that successful run last week?"
- "How can I replicate the exact configuration from my previous experiments?"
- "Is there an easy way to audit how my script has been used over time?"
- "How can I track my program's performance changes depending on its parameters?"

`argparse-history` is here to solve these problems and more!

## What is `argparse-history`?

`argparse_h.ArgumentParser` is an extension of Python's built-in `argparse.ArgumentParser` that automatically tracks and stores the command-line arguments used in your scripts. It's designed to be a drop-in replacement for ArgumentParser, adding powerful history tracking capabilities with minimal changes to your existing code.

## Key Features

- 📜 Automatic command history tracking
- 🕰️ Timestamped entries for easy reference
- 🔍 Built-in history viewing functionality
- 🔍 Tracking execution statistics, or any other relevant data depending on the arguments
- 📁 Customizable history file location
- 🔌 Seamless integration with existing argparse code

## Installation

Install `argparse-history` with pip:

```bash
pip install argparse-history
```

## Quick Start
Replace your existing `ArgumentParser` with `argparse_h.ArgumentParser`:

```python
from argparse_h import ArgumentParser

parser = ArgumentParser(description="Your script description")
parser.add_argument('--input', help='Input file', required=True)
parser.add_argument('--output', help='Output file', required=True)

args = parser.parse_args()

# Your script logic here

```

That's it! Your script now tracks command history automatically.

### Viewing Command History
To view the command history, simply run your script with the --show-history flag:

```bash
python your_script.py --show-history
```

This will display a list of previous runs with their timestamps and arguments.

```bash
python your_script.py --show-args "2024-10-04T10:30:00"
```

This will display the command line that corresponds to the timestamp `"2024-10-04T10:30:00"` 
(that you hopefully copy-pasted from `--show-history` output!)

```bash
python your_script.py --show-stats
```

In addition to the arguments history this will display any data saved during program runs (see below
how to add your performance data to the history).


#### Customizing History File Location

By default, the history is stored in the current directory. You can specify a custom directory:

```bash
python your_script.py --input in.txt --output out.txt --history-dir /path/to/history
```

### Play with the provided example!

- Basic usage:

```bash
python test_argparse.py 80 -n 42 -s hello --flag -l item1 -l item2
```

should yield:

```bash
Parsed arguments:
  m: 80
  number: 42
  string: hello
  flag: True
  list: ['item1', 'item2']
  
Computation result: 1764
```

- Show history:
```bash
python test_argparse.py --show-history
```

gives something like:

```bash
Timestamp: 2024-10-04T17:47:38
Arguments:
  show_args: None
  number: 42
  string: hello
  flag: True
  list: ['item1', 'item2']

Timestamp: 2024-10-04T17:49:25
Arguments:
  show_args: None
  number: 42
  string: hello
  flag: True
  list: ['item1', 'item2']
```

- Show stats:
```bash
python test_argparse.py --show-stats
```

yields something like:

```bash
Timestamp: 2024-10-04T17:47:38
Arguments:
  show_args: None
  number: 42
  string: hello
  flag: True
  list: ['item1', 'item2']
Statistics:
  No statistics recorded

Timestamp: 2024-10-04T17:49:25
Arguments:
  show_args: None
  number: 42
  string: hello
  flag: True
  list: ['item1', 'item2']
Statistics:
  execution_time: 1.5s
  memory_usage: 100MB
```


### How to add your script performance statistics?

- Just call `parser.add_data()` with a dictionary of parameters to save! This is how 
it is done in the example script: 

```python
from argparse_h import ArgumentParser
...
# Simulate adding some stats
parser.add_data({"execution_time": "1.5s", "memory_usage": "100MB"})
```

- For a slightly more complex example within a class:

```python
from argparse_h import ArgumentParser


class MyProcessorClass:
    # your class methods....
    def process(self):
        # Perform operations
        # .....
        self.execution_data = {'n_procs': n_procs, 'cpu time': cpu_time, 'elapsed time': elapsed_time}

    # ......


if __name__ == '__main__':
    # .....
    parser = ArgumentParser(...)
    # ....
    processor = MyProcessorClass(...)
    processor.process()
    # ....
    parser.add_data(processor.execution_data)
```

After you run your script, this will allow you to run: 
```bash
python your_script.py --show-stats
```
and to track your performance data depending on the script arguments. 


## Why Choose argparse-history?

1. Effortless Integration: Minimal changes to your existing code.
2. Improved Reproducibility: Easily recreate previous runs.
3. Better Debugging: Quickly identify what parameters were used in past executions.
4. Audit Trail: Keep track of how and when your script is being used.
5. Execution statistics: keep track of your script performance, or any other relevant data, depending on its parameters.
5. Time-Saving: No more manual logging of script parameters.

## Contributing
Your contributions are welcome! Please feel free to share if you use `argparse-history` and how it is useful to you. 
Also let me know if you have any suggestions of how it could serve you even better!

## License

This project is licensed under the MIT License - see the LICENSE file for details. Start tracking your command history today with argparse_h!

## Functional requirements

- The arguments 'show_history', 'show_stats', 'show_args', 'history_dir' are not recorded to history
- The arguments 'show_history', 'show_stats', 'show_args', 'history_dir' are not listed by the class method
`print_args()` 
- If one of ['show_history', 'show_stats', 'show_args', 'history_dir'] is provided the program stops after 
performing the corresponding actions
- Arguments are stored in their short form
- Arguments are shown by `--show-args` with their leading '-', so that the command line is ready for execution
- Positional (mandatory) arguments are listed by show_args() without their names, just values
