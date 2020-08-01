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
	pwm.write(10)#en grados
	time.sleep(3)
	pitch, roll, yaw = self.getPitchRollYaw()
	if sys.argv[1] == "pitch":
		print("  Pitch: ", pitch, "grados")
	else:
	 	print("  Roll: ", pitch, "grados")
	incl = incl+10

print("- inclinacion de +45 grados")
pwm.write(45)
time.sleep(3)
pitch, roll, yaw = self.getPitchRollYaw()
if sys.argv[1] == "pitch":
	print("  Pitch: ", pitch, "grados")
else:
 	print("  Roll: ", pitch, "grados")

print("- inclinacion de + 40 grados")
pwm.write(40)
time.sleep(3)
pitch, roll, yaw = self.getPitchRollYaw()
if sys.argv[1] == "pitch":
	print("  Pitch: ", pitch, "grados")
else:
 	print("  Roll: ", pitch, "grados")

while incl > -45:
	print("- inclinacion de -", incl ," grados")
	pwm.write(10)
	time.sleep(3)
	pitch, roll, yaw = self.getPitchRollYaw()
	if sys.argv[1] == "pitch":
		print("  Pitch: ", pitch, "grados")
	else:
	 	print("  Roll: ", pitch, "grados")
	incl = incl-10

print("- inclinacion de -45 grados")
pwm.write(-45)
time.sleep(3)
pitch, roll, yaw = self.getPitchRollYaw()
if sys.argv[1] == "pitch":
	print("  Pitch: ", pitch, "grados")
else:
 	print("  Roll: ", pitch, "grados")

pwm.write(0) #dejamos a 0 la inclinacion
