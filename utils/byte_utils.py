from model.pod import Pod


def convert_bytes_to_list_of_string(data: bytes) -> list[str]:
    return data.decode().split("\n")[:-1]
