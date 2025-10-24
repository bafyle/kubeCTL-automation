import logging
from listing import ResourceType, get_all_resources_of_current_namespace_in_list, print_specific_deployment_details
from model.namespace import Namespace
from utils import run_command
from utils.byte_utils import convert_bytes_to_list_of_string
from utils.string_utils import extract_deployment_name, get_user_input_in_integer


def scale_deployment(current_namespace_object: Namespace, current_config: str) -> None:
    all_deployments = get_all_resources_of_current_namespace_in_list(current_namespace_object, current_config, ResourceType.DEPLOYMENT)
    if not len(all_deployments):
        logging.info("No deployments found")
        return
    all_deployments = all_deployments[1:]
    all_deployments = list(map(extract_deployment_name, all_deployments))
    print("Select which deployment do you want to get its logs")
    for index, deployment in enumerate(all_deployments):
        print(f"{index + 1}- {deployment}")
    deployment_number = get_user_input_in_integer(1, len(all_deployments))
    print("Enter the new number of pods desired (0-10 inclusive)")
    pods_scale = get_user_input_in_integer(0, 10)
    deployment_name = all_deployments[deployment_number - 1]
    command = ["kubectl", "scale", "deployment", deployment_name, f"--replicas={pods_scale}", '-n', current_namespace_object.name, f'--kubeconfig={current_config}']
    _, std_out, std_err = run_command(command, shell=False,)
    if bool(std_err):
        error_string = convert_bytes_to_list_of_string(std_err)
        logging.error('\n'.join(error_string))
        return
    output =  convert_bytes_to_list_of_string(std_out)
    print(f"kubectl output: {output[0]}")
    print_specific_deployment_details(current_namespace_object, current_config, deployment_name)
    



