# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import uav
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import math
import socket #instalacion: pip install sockets
import time

r = 6371 #radio de la tierra en km
cont=0
points = [(0,0)]#la primera coordenada siempre coincide con 0,0
headings = []

x = []
y = []
zx = []
z = []

fig, axs = plt.subplots(nrows=2,ncols=2,subplot_kw=dict(projection="3d"), num ='Representación 3d')
fig.canvas.manager.full_screen_toggle()


gs = axs[1, 0].get_gridspec()

axs[0,1].remove()
axs[1,0].remove()
axs[1,1].remove() #borramos subplots para cambiarlos de forma
    
axbig = fig.add_subplot(gs[1,0:])
ax11 = fig.add_subplot(gs[0,1])

axs[0][0].set_title('Representación 3D(m)')
ax11.set_title('Representación 2D(m)')
axbig.set_title('Altura(m)')

fig.tight_layout()

#figs, axs[0][0] = plt.subplots(subplot_kw=dict(projection="3d"), num ='Representación 3d')
quiver=axs[0][0].quiver([],[],[],[],[],[])
axs[0][0].set_xlim(-5, 5)
axs[0][0].set_ylim(-5, 5)
axs[0][0].set_zlim(0, 10)
axs[0][0].set_xlabel('x (norte(-))')
axs[0][0].set_ylabel('y (Este)')
axs[0][0].set_zlabel('z (altura)')

axbig.set_ylim(0,20)
axbig.set_xlim(0,1000)



def heading(c1, c2):
    c1 = (math.radians(c1[0]),math.radians(c1[1]))
    c2 = (math.radians(c2[0]),math.radians(c2[1]))
    difLong = c2[1]-c1[1]
    
    x = math.cos(c2[0])*math.sin(difLong)
    y = math.cos(c1[0])*math.sin(c2[0])-math.sin(c1[0])*math.cos(c2[0])*math.cos(difLong)
    bearing = math.atan2(x,y)
    return round(math.degrees(bearing),2)

def distanciaGPS(c1, c2):
    c1 = (math.radians(c1[0]),math.radians(c1[1]))
    c2 = (math.radians(c2[0]),math.radians(c2[1]))
    difLat = c2[0] - c1[0]
    difLong = c2[1] - c1[1]
    a = (math.sin(difLat/2))**2 + math.cos(c1[0])*math.cos(c2[0])*(math.sin(difLong/2))**2
    c = 2*math.asin(math.sqrt(a))
    return c*r*1000

def GPStoCartesian(bearing, dist, coordsAct):
    x2 = coordsAct[0] + dist * math.cos(bearing)
    y2 = coordsAct[1] + dist * math.sin(bearing)
    return (x2, y2)


"""Crea un server socket y mediante tcp recibe informacion sobre el vuelo, la decodifica
 y la devuelve como parametro"""
def run():
  global coords
  TCP_IP = '192.168.1.35' #dir ip
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

  data = c.recv(BUFFER_SIZE).decode(encoding="utf8", errors='ignore') #recibimos mensaje
  c.close() #cerramos conexion

  data = data[2:] #eliminamos primera y segunda letra que son chars no validos 
 
  altura, c = convertStr(data); #decodificamos informacion
  #print ("altura", altura)
  #print ("coordenadas", c)
  coords = c
  #return altura,c

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

run() 

for i in range (len(coords)-1):
    d = distanciaGPS(coords[i],coords[i+1])
    b = heading(coords[i],coords[i+1])
    headings.append(b)
    c = GPStoCartesian(math.radians(b),d,points[i]) #cambiar
    points.append(c)
  
print('coords: ',coords)
print('points: ',points)
print('headings: ',headings)

for i in range (len(points)): #pintamos en el plano los puntos de la app
    axs[0][0].scatter(-points[i][0],points[i][1], marker="o")
    axs[0][0].text(-points[i][0],points[i][1],0, str(coords[i]))
    ax11.scatter(-points[i][0],points[i][1], marker="o")
    ax11.annotate(i,(-points[i][0],points[i][1]))


def prepro(sol):
    #extremos los datos que corresponden a la posición.
    p = sol.y[3:6,:]
    #extraemos de los datos en y la matriz de rotación que nos define la
    #actitude del dron respecto a un sistema NED fijo a tierra
    n_datos = sol.y.shape[1]
    #construimos un array con las n_datos matrices de rotacion obtenidas
    #durante una simulación 
    R = np.transpose(sol.y[6:15,:].reshape(3,3,n_datos),(2,1,0))
    
    #Matriz de rotación a coordenadas tierra x y z planas z es positivo para
    #es un giro de 180 grados en torno al eje y de las coordenas NED
    RL=np.array([[-1,0,0],[0,1,0],[0,0,-1]])    

    #rotamos a coordenadas tierra las posiciones
    pt = np.dot(RL,p)
    frame = zip(pt.T,R)
    return frame

sol, sol2 = uav.simulador(puntos=points, angulos=headings) #INCLUIR PARAMS

frame =prepro(sol)

def update(i):
    global quiver
    global cont
    global zx
    global z
    
    quiver.remove()
    RL=np.array([[-1,0,0],[0,1,0],[0,0,-1]])  
    v = np.dot(RL,i[1])
    h = v[0,:]+v[1,:]
    h[2]=0
    h=h/np.linalg.norm(h)
    #h = h/np.linalg.norm(h)
    axs[0][0].set_xlim(-5+i[0][0], 5+i[0][0])
    axs[0][0].set_ylim(-5+i[0][1], 5+i[0][1])
    axs[0][0].set_zlim(0, 10)  
    quiver=axs[0][0].quiver(i[0][0],i[0][1],i[0][2],np.append(v[0,:],h[0]),\
                     np.append(v[1,:],h[1]),np.append(v[2,:],h[2]),\
                     normalize=True,color=('r','g','b','k'))

    x.append(i[0][0])
    y.append(i[0][1])
    z.append(i[0][2])
    zx.append(cont)
    
    axbig.set_ylim(0,20)
    axbig.set_xlim(0,500+cont)

    ax11.plot(x,y,color='green')
    axbig.plot(zx,z,color='grey')
    cont+=1
    plt.pause(0.05)


ani = animation.FuncAnimation(fig, update,frames=frame, interval=10,\
                              save_count = 1000)


plt.show()
