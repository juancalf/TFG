
#!/usr/bin/env python
#instalacion: pip install sockets

import socket
import time

 
def run(mpu):
  Mpu = mpu
  info = (0.3, 0.9, 14.5, 1300) #(pitch, roll, yaw, h)
  ready = False

  TCP_IP = '192.168.1.74' #debe ser estatica
  TCP_PORT = 12345
  BUFFER_SIZE = 1024

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  print("servidor listo, esperando clientes")
  time.sleep(1)
  c,d = s.accept()
  print("un cliente se ha conectado")
  while not ready:

    data = c.recv(BUFFER_SIZE).decode() ##elimina los caracteres raros
    if not data: break
    print ("received data:", data)
  	
    if data == 'SndInfo':
     print ("SndInfo detectado")
     #c.sendall(str(info).encode())##el encode convierte a bytes los str
     c.sendall(str(Mpu.getPitchRoll()).encode())

    elif str(data).startswith('Coords'):
      print("coordenadas recibidas")
      c.sendall(str('fin').encode())
      ready = True

    else:
     print ("comando desconocido")

  print("cliente desconectado")
  c.close()
  return str(data)