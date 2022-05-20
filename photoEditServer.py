import io
import socket
from PIL import Image, ImageFilter
from PIL.ImageFilter import EDGE_ENHANCE

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))  # 127.0.0.1
server.listen(5)
BUFFER_SIZE = 4096

# Receiving image bytes from client then apply the filter on it and save a copy
while True:
    client_socket, _ = server.accept()
    # display client address
    print("CONNECTION FROM:", str(_))
    file_stream = io.BytesIO()
    recv_data = client_socket.recv(BUFFER_SIZE)
    # Receiving image bytes from client and save a copy to edit it
    while recv_data:
        file_stream.write(recv_data)
        recv_data = client_socket.recv(BUFFER_SIZE)
        if recv_data == b"%IMAGE_COMPLETED%":
            break

    image = Image.open(file_stream)
    # Different editing effects: Blurring - Sharpen - Oil - Sketch - Rotate
    # image = image.filter(SHARPEN)
    # image = image.rotate(90)
    # image = image.filter(CONTOUR)

    # applying a filter on the image received
    image = image.filter(ImageFilter.GaussianBlur(radius=10))
    image.save('server_image.jpg')
    break

    # sending the image back to the client after editing it.
with open('server_image.jpg', 'rb') as file:
    file_data = file.read(BUFFER_SIZE)
    while file_data:
        client_socket.sendall(file_data)
        file_data = file.read(BUFFER_SIZE)

    client_socket.send(b"%IMAGE_COMPLETED%")
    server.close()
