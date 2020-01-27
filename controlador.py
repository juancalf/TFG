import acelerometro
import tcpSocket

mpu = acelerometro.MPU()
coords = tcpSocket.run(mpu)
print (coords)
