import sys
import time
import threading
import navio.pwm
import navio.util

class Pwm:

    # puertos gpio pwm navio2
    ESC_INPUT_1 = 12
    ESC_INPUT_2 = 0
    ESC_INPUT_3 = 2
    ESC_INPUT_4 = 10

    # controladores pwm
    pwm_1 =  navio.pwm.PWM(self.ESC_INPUT_1)
    pwm_2 =  navio.pwm.PWM(self.ESC_INPUT_2)
    pwm_3 =  navio.pwm.PWM(self.ESC_INPUT_3)
    pwm_4 =  navio.pwm.PWM(self.ESC_INPUT_4)

    # valores de throttle
    SERVO_MIN = 1.000 #ms -> 0%
    SERVO_MAX = 2.000 #ms -> 100%

    # valores de throttle actuales (por defecto empiezan apagados)
    motor1 = self.SERVO_MIN
    motor2 = self.SERVO_MIN
    motor3 = self.SERVO_MIN
    motor4 = self.SERVO_MIN

    # otras variables
    calibrado = False 
    funcionando = False 
    thread = threading.Thread(target=self._loop_)


    def __init__(self):
        navio.util.check_apm()

        self.pwm_1.initialize()
        self.pwm_2.initialize()
        self.pwm_3.initialize()
        self.pwm_4.initialize()

        # por defecto periodo de 50hz
        self.pwm_1.set_period(50)
        self.pwm_2.set_period(50)
        self.pwm_3.set_period(50)
        self.pwm_4.set_period(50)

        self.pwm_1.enable()
        self.pwm_2.enable()
        self.pwm_3.enable()
        self.pwm_4.enable()

    """fucion paralela para el movimiento de los motores"""
    def _loop_(self):
        while self.funcionando:
            self.pwm_1.set_duty_cycle(self.motor1)
            self.pwm_2.set_duty_cycle(self.motor2)
            self.pwm_3.set_duty_cycle(self.motor3)
            self.pwm_4.set_duty_cycle(self.motor4)

    """funcion usada para variar la velocidad de los motores"""
    def aplicarThrottle(self,m1,m2,m3,m4):
        self.motor1 = self.m1
        self.motor2 = self.m2
        self.motor3 = self.m3
        self.motor4 = self.m4

    """funcion para arrancar los motores, llama a _loop_ en otro hilo"""
    def conectarMotores(self):
        self.funcionando = True
        self.thread.start()

    """funcion de calibracion, se debe llamar antes de usar los motores"""   
    def calibracion(self):
        self.aplicarThrottle(self.SERVO_MAX,self.SERVO_MAX,self.SERVO_MAX,self.SERVO_MAX) # 100%
        print ("ESCs nivel maximo")
        print("conectar bateria")
        time.sleep(10) ## esperamos 10s a que los variadores confirmen
        self.aplicarThrottle(self.SERVO_MIN,self.SERVO_MIN,self.SERVO_MIN,self.SERVO_MIN) # 0% 
        print ("ESCs nivel minimo")
        time.sleep(10)
        self.aplicarThrottle(1.100,self.SERVO_MIN,self.SERVO_MIN,self.SERVO_MIN) # 10%
        time.sleep(5)
        self.aplicarThrottle(1.100,1.100,self.SERVO_MIN,self.SERVO_MIN)
        time.sleep(5)
        self.aplicarThrottle(1.100,1.100,1.100,self.SERVO_MIN)
        time.sleep(5)
        self.aplicarThrottle(1.100,1.100.100,1.100,1.100)
        time.sleep(5)
        #apagamos motores
        self.aplicarThrottle(self.SERVO_MIN,self.SERVO_MIN,self.SERVO_MIN,self.SERVO_MIN)
        print ("calibracion completada")

    """usada al finalizar el recorrido para desconectar el controlador pwm"""
    def desconectarMotores(self):
        self.funcionando = False
        self.thread.join()


