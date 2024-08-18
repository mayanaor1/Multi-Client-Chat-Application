# Multi-Client-Chat-Application
## Description
This is a simple multi-client chat application implemented in Python using socket programming. It consists of a server and a client component, allowing multiple users to join or create chat groups.
## Features

* Create new chat groups
* Join existing chat groups
* Password-protected chat groups
* Multiple simultaneous chat groups
* Real-time message broadcasting within groups

## Files

* server.py: The server-side script
* client.py: The client-side script

## Requirements

* Python 3.x
* Socket library (built-in)
* Threading library (built-in)

## Usage
### Starting the Server

1. Run the server script
```
python server.py
```

2. The server will start and listen for incoming connections.

### Running a Client

1. Run the client script:
```
Copypython client.py
```

2. Follow the on-screen prompts to:

* Connect to an existing chat group
* Create a new chat group
* Exit the server



## How It Works

* The server manages multiple chat groups and client connections.
* Clients can create new groups or join existing ones with a password.
* Messages are broadcasted to all members of a group in real-time.

## Authors

Maya Naor (315176362)

Adina Hessen (336165139)

## Notes

The application uses localhost (127.0.0.1) and port 7037 by default.

Ensure the port is not in use by other applications.


## License
This project is provided as-is, without any express or implied warranty. Use at your own risk.
