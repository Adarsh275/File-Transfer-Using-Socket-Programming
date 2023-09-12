# File Transfer Using Socket Programming

A simple client-server program to transfer files between computers as bytes (NOT TCP).

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
