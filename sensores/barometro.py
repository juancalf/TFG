import time
import navio.ms5611
import navio.util

class Barometer:

	baro = navio.ms5611.MS5611()

	def ini(self):
		navio.util.check_apm()
		self.baro.initialize()

	def getAltitude(self, muestras, decimales): #filtro de media movil
		presiones = []
		for i in range(0,muestras):
		 presiones.append(self._getPress_()) #cmp
		 time.sleep(0.01) #mirar si podemos quitarlo #cmp

		presionRef = sum(presiones)/muestras
		return round(self._getAltitude_(presionRef), decimales)

	def _getAltitude_(self, pressure):
		return 44330 * (1 - (pressure / 1013.25)**(1/5.255))

	def _getPress_(self):
		self.baro.refreshPressure()
		time.sleep(0.01) # Waiting for pressure data ready 10ms
		self.baro.readPressure()

		self.baro.refreshTemperature()
		time.sleep(0.01) # Waiting for temperature data ready 10ms
		self.baro.readTemperature()

		self.baro.calculatePressureAndTemperature()
		return self.baro.PRES
