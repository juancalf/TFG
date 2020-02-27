import spidev
import time
import argparse
import sys
import navio.util
from Complementary_Filter import comp_filt

navio.util.check_apm()

posicion = comp_filt()
posicion.init()

#De los dos sensores usamos el lsm que es mas preciso
#imu = navio.mpu9250.MPU9250()
imu = navio.lsm9ds1.LSM9DS1()

if imu.testConnection():
    print "Connection established: True"
else:
    sys.exit("Connection established: False")

imu.initialize()
time.sleep(1)

while 1:
	m9a, m9g, m9m = imu.getMotion9()

	posicion.attitude3(float(m9a[0]),float(m9a[1]),float(m9a[2]),float(m9g[0]),float(m9g[1]),
		float(m9g[2]),float(m9m[0]),float(m9m[1]),float(m9m[2]))

	roll = -posicion.pitch_d
	pitch = -posicion.roll_d
	yaw = posicion.yaw_d
	print "pitch", pitch
	print "roll", roll
	print "yaw" , yaw
	posicion.reset()
	time.sleep(0.5)