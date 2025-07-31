import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

client = None


def start_server():
    global client
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind((socket.BDADDR_ANY, 4))
    server.listen(1)
    server_log.insert(tk.END, "Server started. Waiting for connection...\n")

    def accept_connection():
        global client
        client, addr = server.accept()
        header_label.config(text=f"Chat with {addr}")
        server_log.insert(tk.END, f"Connected to {addr}\n")

        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                server_log.insert(tk.END, f"Client: {data.decode('utf-8')}\n", "received")
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
        server_log.insert(tk.END, f"You: {message}\n", "sent")
        message_entry.delete(0, tk.END)
    else:
        server_log.insert(tk.END, "No client connected.\n")


root = tk.Tk()
root.title("Bluetooth Chat Server")

# Header Frame
header_frame = tk.Frame(root, bg="#1E3A8A", height=50)  # Blue background
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="Bluetooth Chat", bg="#1E3A8A", fg="white", font=("Helvetica", 16))
header_label.pack(pady=10)

# Chat Log (ScrolledText)
server_log = scrolledtext.ScrolledText(root, width=50, height=20, bg="#E0E7FF", fg="black", font=("Helvetica", 12),
                                       wrap=tk.WORD)  # Light blue background
server_log.pack(padx=10, pady=(0, 10))

server_log.tag_config("sent", foreground="white", background="#3B82F6")  # Sent messages in blue
server_log.tag_config("received", foreground="black", background="#DBEAFE")  # Received messages in lighter blue

# Message Entry Frame
message_frame = tk.Frame(root, bg="#E0E7FF", pady=10)  # Light blue background
message_frame.pack(fill=tk.X, padx=10)

message_entry = tk.Entry(message_frame, width=40, font=("Helvetica", 12), bg="white", bd=0)
message_entry.pack(side=tk.LEFT, padx=(0, 10))

send_button = tk.Button(message_frame, text="Send", bg="#2563EB", fg="white", font=("Helvetica", 12),
                        command=send_message)  # Blue send button
send_button.pack(side=tk.LEFT)

start_server_button = tk.Button(root, text="Start Server", command=start_server, bg="#3B82F6", fg="white",
                                font=("Helvetica", 12))
start_server_button.pack(pady=10)

root.geometry("400x600")
root.configure(bg="#E0E7FF")  # Light blue background
root.mainloop()
