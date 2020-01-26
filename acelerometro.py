# uso del MPU9250
import spidev
import time
import argparse
import sys
import navio.mpu9250
import navio.util
import math

class MPU:

	mpu = navio.mpu9250.MPU9250()

	def ini(self):
		navio.util.check_apm()
		self.mpu.initialize()
		time.sleep(1)
		self.mpu.calib_mag()
		if self.mpu.testConnection():
			print ("Conexion establecida")
			return True
		else:
			sys.exit("Error: no conectado")
			return False

	def getPitchRoll(self):
		self.mpu.read_acc()
		acc_x = self.mpu.accelerometer_data[0]
		acc_y = self.mpu.accelerometer_data[1]
		acc_z = self.mpu.accelerometer_data[2]
		roll = math.degrees(math.atan(acc_y/acc_z))
		pitch = math.degrees(math.atan((-acc_x)/math.sqrt(acc_y**2 + acc_z**2)))
		return pitch, roll

	def getPitchRollRad(self):
		self.mpu.read_acc()
		acc_x = self.mpu.accelerometer_data[0]
		acc_y = self.mpu.accelerometer_data[1]
		acc_z = self.mpu.accelerometer_data[2]
		roll = math.atan(acc_y/acc_z)
		pitch = math.atan((-acc_x)/math.sqrt(acc_y**2 + acc_z**2))
		return pitch, roll