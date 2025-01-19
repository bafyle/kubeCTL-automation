import subprocess
import sys
from constants import *
import os
import logging
import re
from model.pod import Pod
from utils.networking import is_port_in_use, get_process_name_for_port
from utils.byte_utils import convert_bytes_list_of_pods, convert_bytes_to_list_of_string
from utils.string_utils import extract_deployment_name, get_user_input_in_integer
from typing import IO, Any
import time

print(f"Python version: {sys.version}\nCurrent date and time: {time.strftime('%I:%M %p %Z on %b %d, %Y')}")

logging.basicConfig(format='LOGGING [%(process)d] [%(levelname)s] %(message)s', level=logging.INFO)

def _run_command(command: list[str], input: str | bytes = None, output: None | int | IO[Any]=subprocess.PIPE, shell=False):
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=output, shell=shell)
    process_output, process_error = process.communicate(input=input)
    return process, process_output, process_error


def get_all_pods_of_current_namespace_in_list(current_namespace: Namespace, current_config: str):
    logging.info("getting all pods...")
    getting_all_pods_command = ['kubectl', 'get', 'pods', '-n', current_namespace.name, f'--kubeconfig={current_config}']
    logging.info(f"running command: {' '.join(getting_all_pods_command)}")

    _, std_out, std_err = _run_command(getting_all_pods_command)

    if(bool(std_err)):
        error_string = convert_bytes_to_list_of_string(std_err)
        logging.error('\n'.join(error_string))
        return []
    return convert_bytes_to_list_of_string(std_out)


def get_all_deployments_of_current_namespace_in_list(current_namespace: Namespace, current_config: str):
    logging.info("getting all deployments...")
    getting_all_pods_command = ['kubectl', 'get', 'deployments', '-n', current_namespace.name, f'--kubeconfig={current_config}']
    logging.info(f"running command: {' '.join(getting_all_pods_command)}")

    _, std_out, std_err = _run_command(getting_all_pods_command)
    std_out, std_err = subprocess.Popen(getting_all_pods_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if(bool(std_err)):
        error_string = convert_bytes_to_list_of_string(std_err)
        logging.error('\n'.join(error_string))
        return []
    return convert_bytes_to_list_of_string(std_out)

def print_all_pods_of_current_environment(current_namespace: Namespace, current_config: str):
    list_of_pods = get_all_pods_of_current_namespace_in_list(current_namespace, current_config)
    if list_of_pods is None:
        return
    printable_string = "\n".join(list_of_pods)
    print(f"all pods: \n{printable_string}", end='')

    
def print_all_deployments_of_current_environment(current_namespace: Namespace, current_config: str):
    list_of_all_deployments = get_all_deployments_of_current_namespace_in_list(current_namespace, current_config)
    if list_of_all_deployments is None:
        return
    printable_string = "\n".join(list_of_all_deployments)
    print(f"all deployments: \n{printable_string}", end='')

def quick_port_forward(current_namespace_object: Namespace, current_config: str):
    namespace_quick_deployments = QUICK_DEPLOYMENTS.get(current_namespace_object.name)
    if namespace_quick_deployments is None:
        print(f"{current_namespace_object.name} doesn't have an DB pod in it")
        return
    
    chosen_deployment = None
    if len(namespace_quick_deployments) > 1:
        print("Choose one of the quick deployments")
        for index, quick_deployment in enumerate(namespace_quick_deployments):
            print(f"{index + 1}- {quick_deployment.description}")
        user_input = get_user_input_in_integer(1, len(namespace_quick_deployments))
        chosen_deployment = namespace_quick_deployments[user_input - 1]
    else:
        chosen_deployment = namespace_quick_deployments[0]

    logging.info(f"starting forwarding port {chosen_deployment.local_machine_port} ...")
    _port_forward(current_namespace_object.name, current_config, chosen_deployment.resource, chosen_deployment.local_machine_port, chosen_deployment.pod_port)


def get_logs(current_namespace: Namespace, current_config: str):
    all_deployments = get_all_deployments_of_current_namespace_in_list(current_namespace, current_config)
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
    opening_text_editor_command = [TEXT_EDITOR_COMMAND, fr"{os.getcwd()}\{LOGFILE_NAME}"]
    _open_log_file(opening_text_editor_command)


def _dump_logs_to_log_file(logs_command: list[str], absolute_file_name: str):
    with open(absolute_file_name, "w+") as logfile:
        process, _, _ = _run_command(logs_command, output=logfile)
        logging.info(f"dumping logs into file is completed (subprocess: {process.pid} is finished with code: {process.returncode})")
    logging.info(f"logfile located in: {os.getcwd()}")


def _open_log_file(command: list[str]):
    logging.info(f"Opening the log file using the command: {' '.join(command)}")
    process, _, _ = _run_command(command, shell=True)
    logging.info(f"subprocess with pid: {process.pid} exited with code: {process.returncode}")


def _port_forward(namespace: str, config: str, resource: str, local_port: int, pod_port: int):
    port_forward_command = ["kubectl", "port-forward", resource, f"{local_port}:{pod_port}", "-n", namespace, f'--kubeconfig={config}']
    port_forward_command_in_string = ' '.join(port_forward_command)
    try:
        while True:
            logging.info("running command: " + port_forward_command_in_string)
            os.system(port_forward_command_in_string)
            connection_lost_time = time.strftime("%I:%M %p")
            print(f"Connection lost on {connection_lost_time}. Enter 1 to retry and 2 to exit")
            user_input = get_user_input_in_integer(1, 2)
            if user_input == 2:
                return
    except KeyboardInterrupt:
        return


def get_pod_active_port(namespace: Namespace, pod: Pod, config: str) -> str:
    logging.info(f"getting active port of pod: {pod}")
    describe_pod_command = ['kubectl', 'describe', 'pod', pod.name, "-n", namespace.name, f'--kubeconfig={config}']
    getting_str_command = ['findstr', 'Port']
    logging.info(f"running command {' '.join(describe_pod_command)}")
    _, output, error = _run_command(describe_pod_command)
    if(bool(error)):
        error_string = convert_bytes_to_list_of_string(error)
        logging.error('\n'.join(error_string))
        exit(1)
    logging.info(f"feeding the output to: {' '.join(getting_str_command)}")
    _, output, _ = _run_command(getting_str_command, input=output)
    port_string = re.search("\d+", output.decode().strip()).group()
    port_int = int(port_string)
    logging.info(f"Port found: {port_string}")
    port_validation = _check_port(port_int)
    if port_validation:
        return port_string
    return


def _check_port(port: int) -> bool:
    while is_port_in_use("127.0.0.1", port):
        process_name_uses_port = get_process_name_for_port(port)
        print(f"Port: {port} is actively being used by: {process_name_uses_port}, close it to continue")
        print("Enter 1 to retry 2 to exit")
        user_input = get_user_input_in_integer(1, 2)
        if user_input == 2:
            return False
    return True



def pod_port_forward(current_namespace: Namespace, current_config: str):
    all_pods = get_all_pods_of_current_namespace_in_list(current_namespace, current_config)
    all_pods = convert_bytes_list_of_pods(all_pods)
    if not len(all_pods):
        return
    print("select which pod do you want to port forward to (only viewing running pods)")
    all_pods = list(filter(lambda x: x.status.lower() == "running", all_pods))
    for index, pod in enumerate(all_pods):
        print(f"{index + 1}- {pod.name}")

    user_input = get_user_input_in_integer(1, len(all_pods))
    selected_pod = all_pods[user_input - 1]
    port = get_pod_active_port(current_namespace, selected_pod, current_config)
    if not port:
        return
    logging.info(f"starting forwarding local port: {port} to pod port {port} ...")
    _port_forward(current_namespace.name, current_config, selected_pod.name, port, port)


if __name__ == "__main__":
    while True:
        print("Which namespace do you want? (DBs are in different namespaces than APIs, except preprod)")
        for key, value in NAMESPACES.items():
            print(f"{key}- {value}")

        user_input = get_user_input_in_integer(1, len(NAMESPACES))

        current_namespace = NAMESPACES.get(user_input)

        current_config = current_namespace.kubeconfig

        logics = {
            1: quick_port_forward,
            2: print_all_pods_of_current_environment,
            3: get_logs,
            4: pod_port_forward,
            5: print_all_deployments_of_current_environment,
        }

        print("Which action do you want ?")

        for key, value in logics.items():
            print(f"{key}- {value.__name__}")

        user_input = get_user_input_in_integer(1, len(logics))

        logics.get(user_input)(current_namespace, current_config)

        print()
