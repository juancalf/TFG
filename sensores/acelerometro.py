## Usamos el sensor LSM9DS1 en lugar del MPU9250

import spidev
import time
import argparse
import sys
import navio.util
import datetime
from Complementary_Filter import comp_filt

class Acelerometro:

    #imu = navio.mpu9250.MPU9250()
    imu = navio.lsm9ds1.LSM9DS1()
    posicion = comp_filt()

    def __init__(self):
        navio.util.check_apm()

        if self.imu.testConnection():
            print "conexion establecida con el imu"
        else:
            sys.exit("error, conexion no establecida con el imu")

        self.imu.initialize()
        time.sleep(1)

        self.posicion.init()

    def getPitchRollYaw(self):
        m9a, m9g, m9m = self.imu.getMotion9()

        self.posicion.attitude3(float(m9a[0]),float(m9a[1]),float(m9a[2]),float(m9g[0]),float(m9g[1]),
        	float(m9g[2]),float(m9m[0]),float(m9m[1]),float(m9m[2]))

        #por la posicion del sensor hacemos los siguientes cambios
        roll = -self.posicion.pitch_d
        pitch = -self.posicion.roll_d
        yaw = self.posicion.yaw_d

        self.posicion.reset()
        return pitch, roll, yaw;

    """funcion de depuracion, muestra pitch, roll y yaw por pantalla hasta
    interrumpir por teclado"""
    def bucleTest(self):
        while True:
            pitch, roll, yaw = self.getPitchRollYaw()

            print "pitch", pitch
            print "roll", roll
            print "yaw" , yaw

            time.sleep(0.5)