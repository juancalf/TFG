#!/usr/bin/env python

import socket #instalacion: pip install sockets
import time

"""Crea un server socket y mediante tcp recibe informacion sobre el vuelo, la decodifica
 y la devuelve como parametro"""
def run():

  TCP_IP = '192.168.1.52' #dir ip
  TCP_PORT = 12345 #puerto tcp
  BUFFER_SIZE = 1024 #tam ventana de datos

  #creamos server socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  print("servidor listo, esperando cliente...")
  time.sleep(1)
  c,d = s.accept() #acepto conexion del cliente
  print("un cliente se ha conectado")

  data = c.recv(BUFFER_SIZE).decode() #recibimos mensaje
  c.close() #cerramos conexion

  data = data[2:] #eliminamos primera y segunda letra que son chars no validos 
 
  altura, coords = convertStr(data); #decodificamos informacion
  print ("altura", altura)
  print ("coordenadas", coords)
  return altura,coords

"""decodifica el mensaje recibido via TCP y devuelve una tupla con la altura
y la lista de coordenadas"""
def convertStr(msg):
	arr = msg.split("|") #separamos por barras
	altura = float(arr[0]) #la altura la convertimos a float
	arr = arr[1:] #todos menos el primero
	coords = []
	for elem in arr: #creamos tupla de floats con la latitud y longitud de los puntos del recorrido
		aux = elem.split(",")
		coords.append((float(aux[0]),float(aux[1])))
	return altura, coords
