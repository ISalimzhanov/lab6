import argparse
import socket
import os
import threading


def send_file(file_name: str, host: str, port: int) -> None:
    """
    :param file_name: name of the file.txt that should be sen
    :param host: server's address
    :param port: server's port
    :return:
    """
    try:
        file_size = os.path.getsize(file_name)
        file = open(file_name, 'r')
    except FileNotFoundError:
        print('There is no such file.txt')
        return

    s = socket.socket()
    s.connect((host, port))
    print(f'Connected to {host} at port {port}')
    s.sendall(len(file_name).to_bytes(1, byteorder='big'))  # sending file_name size
    s.sendall(file_name.encode())  # sending file.txt name
    sent_size = 0
    buff_size = 1024
    data = file.read(buff_size)
    while data:  # sending file.txt
        s.send(data.encode())
        data = file.read(buff_size)
        sent_size = min(sent_size + buff_size, file_size)
        print(f'progress: {sent_size}/{file_size} bytes are sent')
    file.close()
    s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", help="name of the file.txt that should be sent", type=str)
    parser.add_argument("--s_host", help="server's address", type=str)
    parser.add_argument("--s_port", help="server's port", type=int)
    args = parser.parse_args()
    thread = threading.Thread(target=send_file, args=(args.file_name, args.s_host, args.s_port))
    thread.start()