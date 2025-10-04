import subprocess
from typing import IO, Any

def run_command(command: list[str], input: str | bytes = None, output: None | int | IO[Any]=subprocess.PIPE, shell=False):
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=output, shell=shell)
    process_output, process_error = process.communicate(input=input)
    return process, process_output, process_error