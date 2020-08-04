# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def posicion(sol):
    fig =plt.figure()
    plt.subplot(3,1,1)
    plt.plot(sol.t,-sol.y[5])    
    plt.xlabel('t')
    plt.ylabel('z(altura)')
    
    plt.subplot(3,1,2)
    plt.plot(sol.t,sol.y[4])    
    plt.xlabel('t')
    plt.ylabel('y(este)')
    
    plt.subplot(3,1,3)
    plt.plot(sol.t,-sol.y[3])    
    plt.xlabel('t')
    plt.ylabel('x(norte)')

def orientacion(sol):
    n_datos = sol.y.shape[1]
    #construimos un array con las n_datos matrices de rotacion obtenidas
    #durante una simulación
    v = sol.y[6:9,:]+sol.y[9:12,:]
    #Eliminimamos componente z porque solo nos interesa la proyección en xy
    v[2,:] = 0
    for i in range(n_datos):
        v[:,i]=v[:,i]/np.linalg.norm(v[:,i])
    #normalizamos
    fig=plt.figure()
    plt.subplot(2,1,1)
    plt.plot(sol.t,v[0])    
    plt.xlabel('t')
    plt.ylabel('x')
    
    plt.subplot(2,1,2)
    plt.plot(sol.t,v[1])    
    plt.xlabel('t')
    plt.ylabel('y')
    
    return v
    
def velocidades(sol):
    
    fig =plt.figure()
    
    plt.subplot(4,1,1)
    plt.plot(sol.t,sol.y[0])    
    plt.xlabel('t')
    plt.ylabel('vx (norte)')
    
    plt.subplot(4,1,2)
    plt.plot(sol.t,sol.y[1])    
    plt.xlabel('t')
    plt.ylabel('vy(este)')
    
    plt.subplot(4,1,3)
    plt.plot(sol.t,sol.y[2])    
    plt.xlabel('t')
    plt.ylabel('vz(down)')
    
    plt.subplot(4,1,4)
    n_datos = sol.y.shape[1]
    #construimos un array con las n_datos matrices de rotacion obtenidas
    #durante una simulación
    v = sol.y[6:9,:]+sol.y[9:12,:]
    #Eliminimamos componente z porque solo nos interesa la proyección en xy
    v[2,:] = 0
    vl=[]
    for i in range(n_datos):
        v[:,i]=v[:,i]/np.linalg.norm(v[:,i])
        vl.append(np.dot([sol.y[0,i],sol.y[1,i],0],v[:,i]))
        
    plt.plot(sol.t,vl)    
    plt.xlabel('t')
    plt.ylabel('v avance')
    
    
def trayectoria(sol):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(-sol.y[3],sol.y[4],-sol.y[5])