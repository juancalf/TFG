# primera version inacabada
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
    pwm_1 =  navio.pwm.PWM(ESC_INPUT_1)
    pwm_2 =  navio.pwm.PWM(ESC_INPUT_2)
    pwm_3 =  navio.pwm.PWM(ESC_INPUT_3)
    pwm_4 =  navio.pwm.PWM(ESC_INPUT_4)

    # valores de throttle
    SERVO_MIN = 1.000 #ms -> 0%
    SERVO_MAX = 2.000 #ms -> 100%

    # valores de throttle actuales (por defecto empiezan apagados)
    motor1 = SERVO_MIN
    motor2 = SERVO_MIN
    motor3 = SERVO_MIN
    motor4 = SERVO_MIN

    # otras variables
    calibrado = False 
    funcionando = False 


    def __init__(self):
        navio.util.check_apm()

        pwm_1.initialize()
        pwm_2.initialize()
        pwm_3.initialize()
        pwm_4.initialize()

        # por defecto periodo de 50hz
        pwm_1.set_period(50)
        pwm_2.set_period(50)
        pwm_3.set_period(50)
        pwm_4.set_period(50)

        pwm_1.enable()
        pwm_2.enable()
        pwm_3.enable()
        pwm_4.enable()

    """funcion de calibracion, se debe llamar antes de usar los motores"""   
    def calibracion(self):
        aplicarThrottle(100,100,100,100) # 100%
        print ("ESCs nivel maximo")
        print("conectar bateria")
        time.sleep(10) ## esperamos 10s a que los variadores confirmen
        aplicarThrottle(0,0,0,0) # 0% 
        print ("ESCs nivel minimo")
        time.sleep(10)
        aplicarThrottle(10,10,10,10) # 10%
        print ("calibracion completada")
        time.sleep(6)
        aplicarThrottle(0,0,0,0)
        funcionando = False ##SOLO PARA DEPURACION

    def _loop_(self):
        while funcionando:
            pwm_1.set_duty_cycle(motor1)
            pwm_2.set_duty_cycle(motor2)
            pwm_3.set_duty_cycle(motor3)
            pwm_4.set_duty_cycle(motor4)

    def aplicarThrottle(self,m1,m2,m3,m4):
        self.motor1 = porcentajeToms(m1)
        self.motor2 = porcentajeToms(m2)
        self.motor3 = porcentajeToms(m3)
        self.motor4 = porcentajeToms(m4)

    def desconectarMotores(self):
        self.funcionando = False;
        ## faltaria un join o algo parecido

    #sin comprobar
    """funcion de conversion de porcentaje a milisegundos""" 
    def porcentajeToms(self,porcentaje):
        if porcentaje < 0 or porcentaje > 100: # 0% - 100%
            sys.exit("error, valores fuera de rango")
        else:
            if porcentaje == 0:
                res = 1.000
            elif porcentaje == 100:
                res = 2.000
            else:
                res = 1.000 + porcentaje*0.01
        return res



