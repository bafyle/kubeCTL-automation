import logging
from utils import run_command
from utils.byte_utils import convert_bytes_to_list_of_string
from model.namespace import Namespace
import enum

class ResourceType(enum.StrEnum):
    DEPLOYMENT = "deployments"
    PODS = "pods"

def print_all_pods_of_current_environment(current_namespace: Namespace, current_config: str):
    list_of_pods = get_all_resources_of_current_namespace_in_list(current_namespace, current_config, ResourceType.PODS)
    if len(list_of_pods) == 0:
        return
    printable_string = "\n".join(list_of_pods)
    print(f"all pods: \n{printable_string}", end='')

    
def print_all_deployments_of_current_environment(current_namespace: Namespace, current_config: str):
    list_of_all_deployments = get_all_resources_of_current_namespace_in_list(current_namespace, current_config, ResourceType.DEPLOYMENT)
    if len(list_of_all_deployments) == 0:
        return
    printable_string = "\n".join(list_of_all_deployments)
    print(f"all deployments: \n{printable_string}", end='')


def print_specific_deployment_details(current_namespace: Namespace, current_config: str, deployment_name: str):
    data = get_specific_deployment_details(current_namespace, current_config, deployment_name)
    if len(data) == 0:
        return
    printable_string = "\n".join(data)
    print(f"deployment details: \n{printable_string}", end='')

def get_specific_deployment_details(current_namespace: Namespace, current_config: str, deployment_name: str):
    getting_all_pods_command = ['kubectl', 'get', 'deployment', deployment_name, '-n', current_namespace.name, f'--kubeconfig={current_config}']
    _, std_out, std_err = run_command(getting_all_pods_command, shell=False,)
    if(bool(std_err)):
        error_string = convert_bytes_to_list_of_string(std_err)
        logging.error('\n'.join(error_string))
        return []
    return convert_bytes_to_list_of_string(std_out)


def get_all_resources_of_current_namespace_in_list(current_namespace: Namespace, current_config: str, resourceType: ResourceType):
    logging.info(f"getting all {resourceType}...")
    getting_all_pods_command = ['kubectl', 'get', str(resourceType), '-n', current_namespace.name, f'--kubeconfig={current_config}']
    _, std_out, std_err = run_command(getting_all_pods_command, shell=False,)

    if(bool(std_err)):
        error_string = convert_bytes_to_list_of_string(std_err)
        logging.error('\n'.join(error_string))
        return []
    return convert_bytes_to_list_of_string(std_out)

