
#!/usr/bin/env python
#instalacion: pip install sockets

import socket
import time
import pitch_roll

mpu = pitch_roll.MPU()
mpu.ini()

#TCP_IP = 'localhost' ##usado solo durante la depuracion
TCP_IP = '192.168.1.69' #tlf ip
TCP_PORT = 12345
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print("conexion realizada")
time.sleep(1)

while True:

  data = s.recv(BUFFER_SIZE) #.decode()
  print ("received data:", data)
	
  if data == 'getTelInfo':
  	     s.sendall(str(mpu.getPitchRoll())) #.encode())

print("cliente desconectado")
s.close()