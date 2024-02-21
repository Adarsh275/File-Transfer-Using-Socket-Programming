# File Transfer Using Socket Programming

A simple client-server program to transfer files between computers as bytes (NOT TCP).
In this project, which is based on socket programming one end user becomes (Server) and another becomes (Client).  Server sends requested files to Client in multiple format (mp4,txt,png,jpeg) and if file is not present in server then server ask client to type a message(requested file name) to client and save it as text file on Server so that it can be made available in future.

# Dependencies

## Virtual Environment

It is preferred to first create a virtual environment and run it in that. (Optional)
```
pip install virtualenv
```
```
python -m virtualenv sockets
```

Run this to activate the environment
```
./sockets/Scripts/activate.ps1
```
or whatever shell it is being run on.

## Installing dependencies

Open the terminal and run
```
pip install -r requirements.txt
```

# Run

- Run server.py on the first machine.
- Run client.py on the second machine.
- Enter the server machine's IP address when prompted in the client machine
- Type the name of the file along with the extension to transfer the file from the server machine to the client machine.

# Note

Developed on python 3.8.10, but should work for older versions of python as well.
