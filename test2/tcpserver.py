import socket
import os
import datetime

print('Server running...')

# Get the current date and time from computer in format: MMDDYYYY-HHMMSS for log file purposes.
dt1 = list(str(datetime.datetime.now()))
dt = dt1
dt[4] = ''
dt[7] = ''
dt[10] = '_'
dt[13] = ''
dt[16] = ''
dt = "".join(dt)
dt = list(dt)
dt[0], dt[4] = dt[4], dt[0]
dt[1], dt[5] = dt[5], dt[1]
dt[2], dt[6] = dt[6], dt[2]
dt[3], dt[7] = dt[7], dt[3]
dt = "".join(dt)

# Truncate dt to 15 bits, 0 - 14.
dt = dt[0:15]

# Rearrange the string to be in HHMMSS-MMDDYYYY
dt = list(dt)
dt.insert(0, dt.pop(8))
dt.insert(0, dt.pop(14))
dt.insert(0, dt.pop(14))
dt.insert(0, dt.pop(14))
dt.insert(0, dt.pop(14))
dt.insert(0, dt.pop(14))
dt.insert(0, dt.pop(14))
dt = "".join(dt)

log_name = 'log_' + dt + '.txt'

tcp_ip = '192.168.0.124' # mac
tcp_port = 6969
buffer_size = 1024  # Normally 1024, but we want fast response so 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((tcp_ip, tcp_port))

#save_path = '/Users/alexnoveloso/Desktop/UHM Archive/EE396F18/ikewai/logs/server_logs'
#save_path = '/Users/alexnoveloso/Desktop/UHM Archive/EE396F18/IkeWaiPc/logs/server_logs'

#save_path = '/Users/alexnoveloso/Desktop/UHM Archive/EE396F18/IkeWaiPc/logs/server_logs'  #REVERT BACK TO THIS ONE
save_path = '/Users/Cyrus/Desktop/demo_log'
completeName = os.path.join(save_path, log_name)
f = open(completeName, 'wb')

s.listen(1)

conn, addr = s.accept()
print('Connection address:'), addr

while True:
    data = conn.recv(buffer_size)
    if not data: break

    while data:
        print("Receiving...")
        f.write(data)
        data = conn.recv(1024)
    f.close()

confirmation = 'Received file...'
print(confirmation)
conn.send(confirmation.encode('utf-8'))
print('Confirmation sent...')

conn.close()
