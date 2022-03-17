import enum
import socket
from pathlib import Path

CURRENT_DIRECTORY = Path.cwd()
SERVER_DIRECTORY = CURRENT_DIRECTORY / 'server_files'
PORT = 12345
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class Status(enum.Enum):
    SUCCESS = '200'
    ERROR = '404'

def search_file(filename):
    file_exists = False
    data = ''
    for item in SERVER_DIRECTORY.iterdir():
        if item.name == filename:
            file_exists = True
            with open(item, 'rb') as f:
                data = f.read()
            break
        else:
           continue
            
    return [data, file_exists]


def create_file(filename, new_data):
    new_file = SERVER_DIRECTORY / filename
    with open(new_file, 'w', encoding=FORMAT) as f:
        f.write(new_data)


def get_file_list():
    files = ''
    for i, item in enumerate(SERVER_DIRECTORY.iterdir(), start=1):
        files += f'{i}: {item.name}\n'
    
    return files


def main():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")

    while True:
        conn, addr = server.accept()
        print('[CONNECTED] Got connection from', addr)
        print(f'[MESSAGE] Sending file list to {addr}')
        conn.send(get_file_list().encode(FORMAT))

        filename = conn.recv(1024).decode(FORMAT)
        print(f'[{addr}] Requesting for {filename}')
        data, file_exists = search_file(filename)

        if file_exists:
            conn.send(Status.SUCCESS.value.encode(FORMAT))
            conn.send(data)
            print(f'[MESSAGE] Requested data sent to {addr}')
            conn.close()
        
        else:
            conn.send(Status.ERROR.value.encode(FORMAT))
            msg = 'File does not exists. Do you want to create one with the same name ? [y/n]: '
            conn.send(msg.encode(FORMAT))
            response = conn.recv(1024).decode(FORMAT)
            print(f'[{addr}] {response}')
            
            if response == 'n':
                conn.close()
            elif response == 'y':
                new_data = conn.recv(1024).decode(FORMAT)
                print(f'[{addr}] New data received')
                create_file(filename, new_data)
                conn.send('The file has been created'.encode(FORMAT))
            else:
                pass

        break


if __name__ == '__main__':
    if not SERVER_DIRECTORY.exists():
        print('[ERROR] Server directory doesn\'t exist\nPlease create a folder called "server_files" with the server files in the directory')
        exit(1)
    
    print('[STARTING] The server is starting..')
    main()
