import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
client.connect(('localhost', 12345))  # 127.0.0.1

BUFFER_SIZE = 4096

# open the image file and send it to the server
with open('client_image.jpg', 'rb') as file:
    file_data = file.read(BUFFER_SIZE)

    while file_data:
        client.send(file_data)
        file_data = file.read(BUFFER_SIZE)
client.send(b"%IMAGE_COMPLETED%")
file.close()

# receive the edited image back from the server
with open("client_edited.jpg", 'wb') as file:
    recv_data = client.recv(BUFFER_SIZE)

    while recv_data:
        file.write(recv_data)
        recv_data = client.recv(BUFFER_SIZE)

        if recv_data == b"%IMAGE_COMPLETED%":
            break
