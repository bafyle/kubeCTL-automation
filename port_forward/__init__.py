import logging 
import time
import os 
import re

from utils.string_utils import get_user_input_in_integer
from utils.byte_utils import convert_bytes_to_list_of_string, convert_bytes_list_of_pods
from utils.networking import is_port_in_use, get_process_name_for_port
from utils import run_command
from listing import get_all_resources_of_current_namespace_in_list, ResourceType
from model.pod import Pod
from model.namespace import Namespace
from constants import QUICK_DEPLOYMENTS



def api_port_forward(current_namespace: Namespace, current_config: str):
    all_pods = get_all_resources_of_current_namespace_in_list(current_namespace, current_config, ResourceType.PODS)
    all_pods = convert_bytes_list_of_pods(all_pods)
    if not len(all_pods):
        return
    print("select which pod do you want to port forward to (only viewing running pods)")
    all_pods = list(filter(lambda x: x.status.lower() == "running", all_pods))
    for index, pod in enumerate(all_pods):
        print(f"{index + 1}- {pod.name}")

    user_input = get_user_input_in_integer(1, len(all_pods))
    selected_pod = all_pods[user_input - 1]
    port = _get_pod_active_port(current_namespace, selected_pod, current_config)
    if not port:
        return
    logging.info(f"starting forwarding local port: {port} to pod port {port} ...")
    _port_forward(current_namespace.name, current_config, selected_pod.name, port, port)


def _get_pod_active_port(namespace: Namespace, pod: Pod, config: str) -> str | None:
    logging.info(f"getting active port of pod: {pod}")
    describe_pod_command = ['kubectl', 'describe', 'pod', pod.name, "-n", namespace.name, f'--kubeconfig={config}']
    logging.info(f"running command {' '.join(describe_pod_command)}")
    _, cleaned_output, error = run_command(describe_pod_command)
    if(bool(error)):
        error_string = convert_bytes_to_list_of_string(error)
        logging.error('\n'.join(error_string))
        exit(1)
    cleaned_output = cleaned_output.decode().strip()
    port_string = re.search(r"Port:\s*(\d+)", cleaned_output).group(1)
    if not port_string:
        logging.error(f"Couldn't find a port string in the following\n{cleaned_output}", )
        return
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