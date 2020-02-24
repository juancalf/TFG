import navio.leds #cmp as led
import navio.util

class Led:
	"""Clase de control del led superior de la placa Navio2"""

	led = navio.leds.Led()

	colors = ['Black', 'Red', 'Green', 'Blue',
	    'Cyan', 'Magenta', 'Yellow', 'White'] ## mirar diferencia con {}


	def setColor(self, color): #cmp mirar la diferencia con cls!
	    navio.util.check_apm()
	    if color in self.colors:
	        self.led.setColor(color)
        else:
	        print("Error, color no definido")

	def turnOff(self):
	    navio.util.check_apm()
	    self.led.setColor('Black')
