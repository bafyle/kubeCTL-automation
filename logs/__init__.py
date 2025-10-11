import logging
import os
import threading
import subprocess
import time

from model.namespace import Namespace
from utils.string_utils import extract_deployment_name, get_user_input_in_integer
from utils import run_command
from constants import *
from listing import get_all_resources_of_current_namespace_in_list, ResourceType


THREAD_SHUTDOWN_SIGNAL = threading.Event()

def get_logs(current_namespace: Namespace, current_config: str):
    all_deployments = get_all_resources_of_current_namespace_in_list(current_namespace, current_config, ResourceType.DEPLOYMENT)
    if not len(all_deployments):
        logging.info("No deployments found")
        return
    all_deployments = all_deployments[1:]
    all_deployments = list(map(extract_deployment_name, all_deployments))
    print("Select which deployment do you want to get its logs")
    for index, deployment in enumerate(all_deployments):
        print(f"{index + 1}- {deployment}")
    user_input = get_user_input_in_integer(1, len(all_deployments))
    current_deployment = all_deployments[user_input - 1]
    kubectl_logs_command = ["kubectl", "logs", f"deployment/{current_deployment}", "-n", current_namespace.name, f"--kubeconfig={current_config}"]
    logging.info(f"running command: {' '.join(kubectl_logs_command)}")
    _dump_logs_to_log_file(kubectl_logs_command, LOGFILE_NAME)
    # opening_text_editor_command = [TEXT_EDITOR_COMMAND, fr"{os.getcwd()}\{LOGFILE_NAME}"]
    opening_text_editor_command = [TEXT_EDITOR_COMMAND, os.path.join(os.getcwd(), LOGFILE_NAME)]
    _open_log_file(opening_text_editor_command)


def _dump_logs_to_log_file(logs_command: list[str], absolute_file_name: str):
    with open(absolute_file_name, "w+") as logfile:
        process, _, _ = run_command(logs_command, output=logfile)
        logging.info(f"dumping logs into file is completed (subprocess: {process.pid} is finished with code: {process.returncode})")
    logging.info(f"logfile located in: {os.getcwd()}")



def _open_log_file(command: list[str]):
    process, _, errors = run_command(command, shell=False)
    logging.info(f"subprocess with pid: {process.pid} exited with code: {process.returncode}")
    if errors is not None:
        logging.info(f"Errors from started process: {errors.decode()}")


def stream_logs(current_namespace: Namespace, current_config: str):
    all_deployments = get_all_resources_of_current_namespace_in_list(current_namespace, current_config, ResourceType.DEPLOYMENT)
    if not len(all_deployments):
        logging.info("No deployments found")
        return
    all_deployments = all_deployments[1:]
    all_deployments = list(map(extract_deployment_name, all_deployments))
    print("Select which deployment do you want to stream its logs")
    for index, deployment in enumerate(all_deployments):
        print(f"{index + 1}- {deployment}")
    user_input = get_user_input_in_integer(1, len(all_deployments))
    current_deployment = all_deployments[user_input - 1]
    kubectl_stream_logs_command = ["kubectl", "logs", f"deployment/{current_deployment}", "-f", "-n", current_namespace.name, f"--kubeconfig={current_config}"]
    _start_stream(kubectl_stream_logs_command, current_deployment)


def _start_stream(kubectl_stream_logs_command: list[str], current_deployment: str):
    THREAD_SHUTDOWN_SIGNAL.clear()
    thread = threading.Thread(target=_stream_stdout_to_file, args=(kubectl_stream_logs_command, STREAM_LOGFILE_NAME), daemon=True)
    thread.start()
    logging.log(logging.INFO, f"Streaming logs for {current_deployment} in separate thread, thread_id: {thread.native_id}")
    logging.log(logging.INFO, "Waiting for the logs file to be created to open")

    while not os.path.isfile(LOGFILE_NAME):
        time.sleep(0.01)
        continue
    logging.log(logging.INFO, f"file found, opening {STREAM_LOGFILE_NAME} with the text editor")
    # opening_text_editor_command = [TEXT_EDITOR_COMMAND, fr"{os.getcwd()}\{STREAM_LOGFILE_NAME}"]
    opening_text_editor_command = [TEXT_EDITOR_COMMAND, os.path.join(os.getcwd(), STREAM_LOGFILE_NAME)]
    _open_log_file(opening_text_editor_command)
    print("Press ctrl-c to stop streaming")
    try:
        while thread.is_alive():
            time.sleep(0.01)
        raise RuntimeError
    except KeyboardInterrupt:
        THREAD_SHUTDOWN_SIGNAL.set()
        thread.join()
    except RuntimeError:
        logging.log(logging.ERROR, "Stream thread shutdown unexpectedly")


def _stream_stdout_to_file(command: list[str], absolute_file_name: str):
    process = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with open(absolute_file_name, "w+") as file:
        for line in iter(lambda: process.stdout.read(4096), b''):
            if THREAD_SHUTDOWN_SIGNAL.is_set():
                file.flush()
                process.stdout.flush
                process.kill()
                break
            file.write(line.decode("utf-8", errors="replace"))
            file.flush()
            process.stdout.flush
        logging.log(logging.INFO, f"Thread ended, process.poll(): {process.poll()}")
