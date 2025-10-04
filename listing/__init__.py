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
    if list_of_pods is None:
        return
    printable_string = "\n".join(list_of_pods)
    print(f"all pods: \n{printable_string}", end='')

    
def print_all_deployments_of_current_environment(current_namespace: Namespace, current_config: str):
    list_of_all_deployments = get_all_resources_of_current_namespace_in_list(current_namespace, current_config, ResourceType.DEPLOYMENT)
    if list_of_all_deployments is None:
        return
    printable_string = "\n".join(list_of_all_deployments)
    print(f"all deployments: \n{printable_string}", end='')


def get_all_resources_of_current_namespace_in_list(current_namespace: Namespace, current_config: str, resourceType: ResourceType):
    logging.info(f"getting all {resourceType}...")
    getting_all_pods_command = ['kubectl', 'get', str(resourceType), '-n', current_namespace.name, f'--kubeconfig={current_config}']
    logging.info(f"running command: {' '.join(getting_all_pods_command)}")

    _, std_out, std_err = run_command(getting_all_pods_command, shell=False,)
    # std_out, std_err = subprocess.Popen(getting_all_pods_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if(bool(std_err)):
        error_string = convert_bytes_to_list_of_string(std_err)
        logging.error('\n'.join(error_string))
        return []
    return convert_bytes_to_list_of_string(std_out)

