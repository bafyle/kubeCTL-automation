from model.pod import Pod

def convert_bytes_list_of_pods(data: bytes) -> list[Pod]:
    list_of_pods = []
    for pod_in_string in data:
        pod_in_string_splitted = pod_in_string.split()
        list_of_pods.append(Pod(pod_in_string_splitted[0], pod_in_string_splitted[1], pod_in_string_splitted[2], pod_in_string_splitted[3], pod_in_string_splitted[4]))
    return list_of_pods

def convert_bytes_to_list_of_string(data: bytes) -> list[str]:
    return data.decode().split("\n")[:-1]
