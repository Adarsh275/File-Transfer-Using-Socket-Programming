import enum
import socket
import cv2
from pathlib import Path

CURRENT_DIRECTORY = Path.cwd()
CLIENT_DIRECTORY = CURRENT_DIRECTORY / 'client_files'
PORT = 12345
SERVER = input('[INPUT] Enter the server IP Address (Hit ENTER to use the default IP): ') or '172.28.64.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class Status(enum.Enum):
    SUCCESS = '200'
    ERROR = '404'

def resize_frame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


def show_received_file(path):

    if path.suffix in ['.jpg', '.png']:
        img = cv2.imread(path.as_posix())
        cv2.imshow(path.stem, resize_frame(img))
        key = cv2.waitKey(0)
        if key == 27: # ESC key
            cv2.destroyAllWindows()
    
    elif path.suffix in ['.mp4', '.mkv']:
        capture = cv2.VideoCapture(path.as_posix())
        while True:
            # reads the image frame by frame and hence will display each frame
            is_true, frame = capture.read()
            if is_true:
                cv2.imshow(path.stem, resize_frame(frame))
                
                key = cv2.waitKey(10)
                if key == 27: # ESC key
                    break
            else:
                print('[MESSAGE] All frames have been displayed..')
                break
        
        cv2.destroyAllWindows()
        capture.release()
    
    else: # Assuming it's a text file
        print('[MESSAGE] Printing the text file..\n')
        print(f'{path.name}\n-----------------------------')
        with open(path, 'rb') as f:
            file_contents = f.read()
        
        print(file_contents.decode(FORMAT))
        print('-----------------------------')
        

def main():
    print('[CONNECTED] Connected to the server')

    file_list = client.recv(1024).decode(FORMAT)
    print(f'\n[{SERVER}] Files present on the server:')
    print(file_list)
    
    filename = input('[INPUT] Enter the filename to be searched for: ')
    client.send(filename.encode(FORMAT))

    while True:
        status = client.recv(1024).decode(FORMAT)
        recv_file_path = CLIENT_DIRECTORY / filename

        if status == Status.SUCCESS.value:
            print(f'[MESSAGE] Receiving the file from {SERVER}....')
            with open(recv_file_path, 'wb') as f:
                while True:
                    chunk = client.recv(512)

                    if not chunk:
                        print('[MESSAGE] Done!')
                        break
                    f.write(chunk)
                
            print('[MESSAGE] The file has been received..')
            show_received_file(recv_file_path)
            break

        elif status == Status.ERROR.value:
            print(f'\n[{SERVER}] {client.recv(1024).decode(FORMAT)}')
            res = input()
            
            if res == 'n':
                client.send(res.encode(FORMAT))
                break
            elif res == 'y':
                client.send(res.encode(FORMAT))
                new_data = input('[INPUT] Enter the file contents: ')
                client.send(new_data.encode(FORMAT))
                print(f'\n[{SERVER}] {client.recv(1024).decode(FORMAT)}')
                break

    client.close()


if __name__ == '__main__':
    if not CLIENT_DIRECTORY.exists():
        CLIENT_DIRECTORY.mkdir()
    main()
