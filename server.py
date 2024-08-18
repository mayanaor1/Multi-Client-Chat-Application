# server.py
# Maya Naor 315176362
# Adina Hessen 336165139

import socket
import threading
import time

PORT = 7037  # The port number used by the network service.
HOST = '127.0.0.1'  # The IP address of the host.
FORMAT = 'utf-8'  # The character encoding method used for text data.
ADDR = (HOST, PORT)  # creating a tuple of IP+PORT

id_counter = 0  # counter for clients.
groups = {}  # dictionary to the groups and their members.


# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple
    print(f"[LISTENING] server is listening on {ADDR}")
    server_socket.listen()  # Server is open for connections

    while True:
        connection, address = server_socket.accept()  # Waiting for client to connect to server.
        thread = threading.Thread(target=handle_client, args=(connection, address))  # Creating new Thread object.
        # Passing the handle func and full address to thread constructor
        thread.start()  # Start the thread to handle new client.


# Function that handles a client connection.
def handle_client(conn, address):
    print('[CLIENT CONNECTED] on address: ', address)  # Printing connection address

    try:
        # global ID count and groups dictionary
        global id_counter
        global groups

        # send main menu options to the client
        conn.send("Hello client, please choose an option:\n 1. Connect to a group chat\n 2.  Create a group chat.\n "
                  "3. Exit the server.\n".encode(FORMAT))

        while True:
            option = conn.recv(1024).decode(FORMAT)  # receive option number.
            if option == '1' or option == '2' or option == '3':  # for valid option
                print(f"[OPTION SELECTED] client from {address} selected option {option}.\n")
                break
            else:  # for invalid option
                print(f"[ERROR] client from {address} selected an invalid option {option}.\n")
                conn.send("please try again!".encode(FORMAT))
                continue

        if option == '1':  # option 1 - connect an existing chat
            if not groups:  # if there is no chat group
                conn.send("You have chosen to connect to a chat, but there are no chats available to connect "
                          "to. You are disconnected from the server, you can try to connect again later, "
                          "bye!".encode(FORMAT))
                print("[ERROR] there are no chats available to connect.\n")
                return

            conn.send("Enter your name: ".encode(FORMAT))  # ask for client's name
            name = conn.recv(1024).decode(FORMAT)

            conn.send("Enter group ID: ".encode(FORMAT))  # ask for group ID
            while True:  # repeat until group ID is valid
                group_id = conn.recv(1024).decode(FORMAT)  # receive group ID
                if group_id not in groups.keys():  # group ID is invalid
                    conn.send("Wrong ID, try again! ".encode(FORMAT))
                else:
                    conn.send("Enter password: ".encode(FORMAT))
                    print(f'[MEMBER REQUEST] Client {name} from {address} want to join group {group_id}.')
                    break

            while True:  # repeat until receive a correct password
                password = conn.recv(1024).decode(FORMAT)
                if groups[group_id]['password'] == password:  # if received the correct password
                    groups[group_id]['connections'].append(conn)  # connect client to the group
                    conn.send(f"Hi {name}! welcome to group {group_id}".encode(FORMAT))
                    print(f"[NEW MEMBER] {name} has joined to group {group_id}. ")

                    broadcast(conn, ['notify message', f'{name}'], group_id)  # send message to group about new member
                    break
                else:  # wrong password
                    conn.send("Wrong password. Please try again! ".encode(FORMAT))

        if option == '2':  # option 2 - create a new chat group

            conn.send("Enter your name: ".encode(FORMAT))  # ask for client's name
            name = conn.recv(1024).decode(FORMAT)

            conn.send("Enter a new password for your group:".encode(FORMAT))  # ask for new password
            password = conn.recv(1024).decode(FORMAT)  # receive password

            groups[str(id_counter)] = {'connections': [conn], 'password': password, 'threads': []}  # create new group

            group_id = str(id_counter)      # save group ID
            id_counter += 1                 # update counter

            print(f'[NEW CHAT] client {name} has created chat. ID: {group_id}.')
            conn.send(f"Chat {group_id} has been created.".encode(FORMAT))

        if option == '3':   # option 3 - di  sconnect from server
            print(f"[ENDING] client on {address} is disconnected. ")
            conn.send("You have disconnected from the server.".encode(FORMAT))
            return

    except Exception as e:      # errors handler
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", address)
        print(e)

    chat = threading.Thread(target=broadcast, args=(conn, name, group_id))  # Creating new Thread object
    groups[group_id]['threads'].append(chat)
    chat.start()


def broadcast(sender, name, group_to_send):     # send messages to the group's members

    try:
        if name[0] == 'notify message':     # message about new member
            for member in groups[group_to_send]['connections']:
                if member != sender:
                    member.send(f'{name[1]} has joined the chat!'.encode(FORMAT))
            return

        while True:     # receive messages and send them to the group
            message = sender.recv(1024).decode(FORMAT)  # receive a message
            for member in groups[group_to_send]['connections']:     # send to other members
                if member != sender:
                    member.send(message.encode(FORMAT))

    except Exception as e:
        print("[ERROR] Something went wrong while sending the message ")
        print(e)


# main function
if __name__ == '__main__':
    IP = socket.gethostbyname(socket.gethostname())  # find my current IP.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket for the server
    print("[STARTING] server is starting...")
    start_server()

    print("THE END!")
