import socket
import os

print('Client running...')

tcp_ip = '192.168.0.125' # mac
tcp_port = 6969
buffer_size = 1024  # Normally 1024, but we want fast response

save_path = '/home/pi/Desktop/ikewai/logs/client_logs'
completeName = os.path.join(save_path, '%s.txt' % log_name)
f = open('file.txt', 'rb')
l = f.read(1024)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((tcp_ip, tcp_port))

while l:
    print('Sending...')
    s.send(l)
    l = f.read(1024)

f.close()

s.shutdown(socket.SHUT_WR)

# s.send(f.encode('utf-8'))
data = s.recv(buffer_size)
s.close()

print('Received data: ', data.decode('utf-8'))
