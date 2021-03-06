import socket
import os
import threading


def store_file(conn, address) -> None:
    """
    Receiving and storing file.txt
    :param address:
    :param conn:
    :return:
    """
    print(f'Receiving file from {address}')
    # getting file_name
    fname_size = int.from_bytes(conn.recv(1), byteorder='big')
    fname = conn.recv(fname_size).decode()

    # checking is there file.txt with the same file.txt name
    cnt = 0
    new_fname = fname  # new file.txt name
    fname_body, fname_format = fname.split('.')
    while os.path.exists(new_fname):
        cnt += 1
        new_fname = f'{fname_body}_copy{cnt}.{fname_format}'
    # receiving data
    file = open(new_fname, 'wb')
    buff_size = 1024
    data = conn.recv(buff_size)
    while data:
        file.write(data)
        data = conn.recv(buff_size)
    file.close()
    print(f'Received {fname}. Stored as {new_fname}')


def server_main():
    s = socket.socket()
    port = 6060
    s.bind(('', port))
    s.listen(10)
    while True:
        conn, address = s.accept()
        thread = threading.Thread(target=store_file, args=(conn, address))
        thread.start()


if __name__ == '__main__':
    server_main()
