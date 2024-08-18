# client.py
# Maya Naor 315176362
# Adina Hessen 336165139

import socket
import threading
import time

PORT = 7037  # The port number used by the network service.
HOST = '127.0.0.1'  # The IP address of the host.
FORMAT = 'utf-8'  # The character encoding method used for text data.
ADDRESS = (HOST, PORT)  # creating a tuple of IP+PORT


# Function that starts the server.
def start_client():
    client_socket.connect((HOST, PORT))  # Connect to server's socket.

    message = client_socket.recv(1024).decode(FORMAT)
    print(message)  # print hello message and present the options

    while True:
        option = input()  # the client enters a number of option
        client_socket.send(option.encode(FORMAT))  # send his choice to server.

        if option == '1' or option == '2' or option == '3':  # for valid option
            break
        else:  # for invalid option
            message = client_socket.recv(1024).decode(FORMAT)
            print(message)
            continue

    message = client_socket.recv(1024).decode(FORMAT)  # print the first message of the option
    print(message)

    if option == '1':  # option 1 - connect an existing chat
        if "no chats available" in message:  # if there is no chat group
            return

        name = input()
        client_socket.send(name.encode(FORMAT))  # send client's name

        message = client_socket.recv(1024).decode(FORMAT)
        print(message)  # print request for group ID

        while True:  # repeat until group ID is valid
            group_id = input()
            client_socket.send(group_id.encode(FORMAT))  # send group ID
            message = client_socket.recv(1024).decode(FORMAT)
            print(message)
            if 'Wrong' not in message:  # if ID is valid
                break

        flag = False
        while not flag:  # repeat until receive  a correct password
            password = input()
            client_socket.send(password.encode(FORMAT))  # send a password
            message = client_socket.recv(1024).decode(FORMAT)
            if "welcome" in message:  # correct password
                print(message)
                flag = True
            else:
                print(message)  # wrong password

    if option == '2':  # option 2 - create a new chat group

        name = input()
        client_socket.send(name.encode(FORMAT))  # send client's name

        print(client_socket.recv(1024).decode(FORMAT))  # print password request
        password = input()
        client_socket.send(password.encode(FORMAT))  # send password
        print(client_socket.recv(1024).decode(FORMAT))  # approve message

    if option == '3':  # option 3 - disconnect from server
        return

    chat = threading.Thread(target=receive, args=(client_socket,))  # Creating new Thread object.
    chat.start()  # Starting the new thread
    send(client_socket, name)
    client_socket.close()  # Closing socket


def receive(client_socket):  # receive messages
    while True:  # listen for new messages
        message = client_socket.recv(1024).decode(FORMAT)
        print(message)


def send(client_socket, name):  # send messages
    while True:
        message = name + ': ' + input()
        client_socket.send(message.encode(FORMAT))


# main function
if __name__ == "__main__":
    # This block of code will only be executed if the script is run directly, not if it is imported
    # as a module.

    IP = socket.gethostbyname(socket.gethostname())
    # Get the host IP of the machine running the script.

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a new socket using the AF_INET address family (for IPv4) and the SOCK_STREAM socket type
    # (for a TCP connection).

    start_client()
    # Call the start_client function to connect to the server and start the chat.
