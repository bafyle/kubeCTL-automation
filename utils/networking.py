import socket
from contextlib import closing
import psutil
   
def is_port_in_use(host: str, port: str) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0

def get_process_name_for_port(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == 'LISTEN':
            return psutil.Process(conn.pid).name()