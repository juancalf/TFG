import sys
import time
import navio.pwm
import navio.util
import acelerometro

##se comprueba que los parametros sean correctos
if len(sys.argv) == 1:
	print("error, faltan parametros")
	sys.exit()
elif sys.argv[1] == "pitch":
	print("Test Pitch")
elif sys.argv[1] == "roll":
	print("Test Roll")
else:
	print("error, parametro desconocido")
	sys.exit()

#inicializamos pwm
pwm = navio.pwm.PWM(5)
pwm.initialize()
pwm.set_period(50)
pwm.enable()
incl = 10

#se va variando la inclinacion
while incl < 45:
	print("- inclinacion de +", incl ," grados")
	write(incl)#en grados
	time.sleep(3)
	pitch, roll, yaw = self.getPitchRollYaw()
	if sys.argv[1] == "pitch":
		print("  Pitch: ", pitch, "grados")
	else:
	 	print("  Roll: ", pitch, "grados")
	incl = incl+10

print("- inclinacion de +45 grados")
write(45)
time.sleep(3)
pitch, roll, yaw = self.getPitchRollYaw()
if sys.argv[1] == "pitch":
	print("  Pitch: ", pitch, "grados")
else:
 	print("  Roll: ", pitch, "grados")

print("- inclinacion de + 40 grados")
write(40)
time.sleep(3)
pitch, roll, yaw = self.getPitchRollYaw()
if sys.argv[1] == "pitch":
	print("  Pitch: ", pitch, "grados")
else:
 	print("  Roll: ", pitch, "grados")
incl = 40
while incl > -45:
	print("- inclinacion de -", incl ," grados")
	write(incl)
	time.sleep(3)
	pitch, roll, yaw = self.getPitchRollYaw()
	if sys.argv[1] == "pitch":
		print("  Pitch: ", pitch, "grados")
	else:
	 	print("  Roll: ", pitch, "grados")
	incl = incl-10

print("- inclinacion de -45 grados")
write(-45)
time.sleep(3)
pitch, roll, yaw = self.getPitchRollYaw()
if sys.argv[1] == "pitch":
	print("  Pitch: ", pitch, "grados")
else:
 	print("  Roll: ", pitch, "grados")

write(0) #dejamos a 0 la inclinacion


def write (inc):
	signal = (inc / 90.0) + 1.5 # convertimos grados a señal pwm
	pwm.set_duty_cycle(signal)
