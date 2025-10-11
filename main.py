import sys
import logging
import time

from constants import *
from utils.string_utils import get_user_input_in_integer

logging.basicConfig(format='LOGGING [%(process)d] [%(levelname)s] %(message)s', level=logging.INFO)


from logs import get_logs, stream_logs
from port_forward import api_port_forward, quick_port_forward
from listing import print_all_deployments_of_current_environment, print_all_pods_of_current_environment
from deployment_scaling import scale_deployment

if __name__ == "__main__":
    print(f"Python version: {sys.version}\nCurrent date and time: {time.strftime('%I:%M %p %Z on %b %d, %Y')}")
    logics = {
        1: quick_port_forward,
        2: print_all_pods_of_current_environment,
        3: get_logs,
        4: stream_logs,
        5: api_port_forward,
        6: print_all_deployments_of_current_environment,
        7: scale_deployment
    }
    while True:
        print("Which namespace do you want? (DBs are in different namespaces than APIs, except preprod)")
        for key, value in NAMESPACES.items():
            print(f"{key}- {value}")

        user_input = get_user_input_in_integer(1, len(NAMESPACES))

        current_namespace = NAMESPACES.get(user_input)

        current_config = current_namespace.kubeconfig

        print("Which action do you want ?")

        for key, value in logics.items():
            print(f"{key}- {value.__name__}")

        user_input = get_user_input_in_integer(1, len(logics))

        logics.get(user_input)(current_namespace, current_config)

        print()
