# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:04:13 2020

@author: abierto
"""
import numpy as np
import matplotlib.pyplot as plt
import uav
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))
quiver=ax.quiver([],[],[],[],[],[])
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(0, 10)
ax.set_xlabel('x (norte(-))')
ax.set_ylabel('y (Este)')
ax.set_zlabel('z (altura)')

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

sol, sol2 = uav.simulador()
frame =prepro(sol)
def update(i):
    #print(i)
    global quiver
    quiver.remove()
    RL=np.array([[-1,0,0],[0,1,0],[0,0,-1]])  
    v = np.dot(RL,i[1])
    h = v[0,:]+v[1,:]
    h[2]=0
    h=h/np.linalg.norm(h)
    #h = h/np.linalg.norm(h)
    ax.set_xlim(-5+i[0][0], 5+i[0][0])
    ax.set_ylim(-5+i[0][1], 5+i[0][1])
    ax.set_zlim(0, 10)  
    quiver=ax.quiver(i[0][0],i[0][1],i[0][2],np.append(v[0,:],h[0]),\
                     np.append(v[1,:],h[1]),np.append(v[2,:],h[2]),\
                     normalize=True,color=('r','g','b','k'))
    
    #quiver=ax.quiver([0],[0],[0],[i],[i],[i])
    
ani = animation.FuncAnimation(fig, update,frames=frame, interval=20,\
                              save_count = 500)
writer = animation.PillowWriter(fps=20)
ani.save('media_vuelta2.gif', writer= writer)
plt.show()