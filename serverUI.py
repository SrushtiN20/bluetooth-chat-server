import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

client = None  # Define client globally


def start_server():
    global client
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind((socket.BDADDR_ANY, 4))
    server.listen(1)
    server_log.insert(tk.END, "Server started. Waiting for connection...\n")

    def accept_connection():
        global client  # Access the global client variable
        client, addr = server.accept()
        server_log.insert(tk.END, f"Connected to {addr}\n")

        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                server_log.insert(tk.END, f"Client: {data.decode('utf-8')}\n")
            except OSError:
                break

        client.close()
        server_log.insert(tk.END, "Client disconnected.\n")

    threading.Thread(target=accept_connection, daemon=True).start()


def send_message():
    global client
    message = message_entry.get()
    if client:
        client.send(message.encode('utf-8'))
        server_log.insert(tk.END, f"You: {message}\n")
        message_entry.delete(0, tk.END)
    else:
        server_log.insert(tk.END, "No client connected.\n")


root = tk.Tk()
root.title("Bluetooth Chat Server")

server_log = scrolledtext.ScrolledText(root, width=50, height=20)
server_log.pack()

message_entry = tk.Entry(root, width=50)
message_entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

start_server_button = tk.Button(root, text="Start Server", command=start_server)
start_server_button.pack()

root.mainloop()
