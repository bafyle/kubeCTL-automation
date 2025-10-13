import subprocess
from typing import IO, Any
import logging

def run_command(command: list[str], input: str | bytes = None, output: None | int | IO[Any]=subprocess.PIPE, shell=False):
    logging.info(f"running command: {' '.join(command)}")
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=output, shell=shell)
    process_output, process_error = process.communicate(input=input)
    return process, process_output, process_error