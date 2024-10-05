# CmdInterface Class Documentation

## Overview
The `CmdInterface` class provides a robust Python interface for interacting with command-line processes in Windows. It is designed to encapsulate command sending and output handling of a single terminal into a simple and clean API that can be easily integrated into larger applications.

## Features
- **Live Context**: Changes in the terminal context by a command persist and the terminal is kept alive.
- **Multiple Instances**: Launching Multiple Instances at the same time does not create interference.
- **Command Isolation**: Ensures that commands sent through the interface are not executed at the same time if sent to the same instance, and outputs are cleanly separated.
- **Boilerplate Removal**: Automatically handles removal of unnecessary startup text from command outputs.
- **Logging Capability**: Offers optional logging of all commands and outputs for debugging and auditing purposes.
- **Safe Cleanup**: Automatically manages subprocess termination to prevent resource leaks.

## Usage

### Instantiation
Create an instance of the `CmdInterface` with optional configurations:

```python
from CmdInterface import CmdInterface

cmd_interface = CmdInterface(nude=True, rm_boilerplate=True, end_signal="END_OF_OUTPUT", log_mode=False)
