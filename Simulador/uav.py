# -*- coding: utf-8 -*-
import numpy as np
import graf
from scipy.integrate import solve_ivp, RK45
import math

g = 9.8 #gravedad m/s2
k = np.array([1.,1.,1.,1.]) #relación par motor con fuerza ascensional
B = np.array([0.5,0.5,0.5,0.5]) #relacion resitencia helice con fuerza ascen 
kB = k/B
b = 2. #coeficiente de rozamiento del dron con el aire
l = 0.185 #longitud brazos del dron en metros
M = np.array([kB,kB*[l,-l,0,0],kB*[0,0,l,-l],[1,1,-1,-1]]) #matriz de fuerzas
#y pares
m = 2.1 #masa del dron en Kg
mmt = [0.2,0.2,0.2,0.2] #masa de los motores en Kg Nota: la masa del dron
#incluye ya la masa de los cuatros motores, aquí se separa para calcular el 
#tensor de inercia J
J =np.array([[l*(mmt[0]+mmt[2]),0,0],[0,l*(mmt[1]+mmt[3]),0],[0,0,l*sum(mmt)]])
Ji =np.linalg.inv(J) #inversa del tensor de inercia
taun = np.ones(4)*g*m/4/kB #pares de equilibrio (pares que tendrían que hacer
#los motores para compensar la gravedad, y mantener el dron en estacionario)

###############Parámetros de control de la dinámica###################
Tf = 3000.#tiempo final de la simulación en segundos 
ch = 0 #rumbo respecto a norte en grados.
cv = 0#velocidad de consigna en m/s (inicialmente vale 0)
ca = 10 #valor de consigna de la altura de vuelo


cCartesianas = []
headings = []
contador = 0#contador de coordenadas


y0 = np.array([0,0,0,\
               0,0,0,\
               1/np.sqrt(2),-1/np.sqrt(2),0,\
               1/np.sqrt(2),1/np.sqrt(2),0,\
               0,0,1.,\
               0,0,0])

    
def controlador(y,ca=0.,ch=45.,cv=0):
    
    #controlador de altura

    ca = -ca 
    kpa =1.5 #constante de error proporcional a la altura
    kda =0.5 #constante de error derivativo a la altura
    
    kph = 1 #constante de error proporcional al rumbo
    kdh = 5 #constante de error derivativo al rumbo
    
    kpv = 0.4 #constante error de velocidad en avante
    kdv = 4 #constante de error en velocidad en avante
    
    dtau = -kpa*np.ones(4)*(ca-y[5]) + kda*y[2]
    
    #controlador de heading o de rumbo si se quiere
    #el heading lo marca la bisectrix de los ejes cuerpo NED del cuadrotor
    #calculamos la matriz de rotación del cuadrotor
    #R= y[6:15].reshape(3,3).T
    
    
    #Vector unitario en la bisectriz
    #v = R[:,0] + R[:,1]
    v = y[6:9]+y[9:12]
    #Eliminimamos componente z porque solo nos interesa la proyección en xy
    v[2] = 0
    #normalizamos
    vn = v/np.linalg.norm(v)
    #creamos la matriz de cambio a un sistema en que vn marca la dir x
    VN =np.array([[vn[0],vn[1]],[-vn[1],vn[0]]])
    #calculamos el p vectorial por la matriz de rumbos,
    chrad = np.pi * ch / 180
    sch = np.sin(chrad)
    cch = np.cos(chrad)
    Mr =np.array([[0, 0, sch],[0, 0, -cch],[-sch, cch, 0]])
    #calculamos el error de rumbo a partir del producto vectorial del vector
    #de rumbo deseado con v, definido más arriba, esto nos da un valor que cre
    #hasta los 90 grados y decrece de nuevo entre 90 y 180. Por eso añadimos
    #el signo del producto escalar que nos indica en qué cuadrante estamos y 
    #y si el error es mayor de 90º
    esc = np.dot(vn,np.array([cch,sch,0]))
    vec = np.dot(Mr,vn)
    
    errum = vec[2]+(esc<0)*np.sign(vec[2])+(esc==-1.)
    derrum = y[17]

    
    #control de velocidad
    
    vel = np.dot(VN,np.array([y[0],y[1]]))
    errvel = np.array([cv,0])-vel
    
    ft = np.sqrt(2)/2
    errdvel =np.dot(np.array([[ft,ft],[-ft,ft]]),np.array([y[15],y[16]]))
    

    kpv2 = 1
    kdv2 = 5
    dtau[0] = dtau[0]\
        - kph*errum - kdh*derrum\
        + kpv*errvel[0] + kdv*errdvel[1] + kpv2*errvel[1] - kdv2*errdvel[0]
    dtau[1] = dtau[1]\
        - kph*errum - kdh*derrum\
        - kpv*errvel[0] - kdv*errdvel[1] - kpv2*errvel[1] + kdv2*errdvel[0]
    dtau[2] = dtau[2]\
        + kph*errum + kdh*derrum\
        - kpv*errvel[0] - kdv*errdvel[1] + kpv2*errvel[1] - kdv2*errdvel[0]
    dtau[3] = dtau[3]\
        + kph*errum + kdh*derrum\
        + kpv*errvel[0] + kdv*errdvel[1] - kpv2*errvel[1] + kdv2*errdvel[0]

    
    return dtau
       
#distancia entre coordenadas cartesianas
def dist(c1, c2):
    d = math.sqrt((c2[0]-c1[0])**2 + (c2[1]-c1[1])**2)
    #print(d)
    return d


def dt(t,y,taun,M,m,b,J,Ji): 
    ''' Esta función esta pensada para construir el vector de derivadas
    temporales de los estados del quadrotor y poder así resolver las
    Ecuaciones diferenciales empleando los solvers de Scipy'''
        
    global ch #bearing
    global contador #contador de coordenadas
    global cv #velocidad
    global ca

    
    if contador == 0: #durante el despegue
            ch = headings[0]
            if dist((y[3], y[4]), (0,0)) < 5: #controlamos velocidad hasta corregir el rumbo
                cv = 1
            else: #sobra
                cv = 2
                contador = 1
    
    elif contador < (len(headings)):#al recorrer puntos intermedios
        if dist((y[3], y[4]), cCartesianas[contador]) < 15:
            cv = 1
        if dist((y[3], y[4]), cCartesianas[contador]) < 1: #distancia de menos de 10 metros 
            ch = headings[contador]
            contador=contador+1
            
            
        if dist((y[3], y[4]), cCartesianas[contador-1])>15 and dist((y[3], y[4]), cCartesianas[contador])>15:
            cv = 2

            
    else:#durante el aterrizaje
         if dist((y[3], y[4]), cCartesianas[contador]) < 10:
            cv = 0.5
            if dist((y[3], y[4]), cCartesianas[contador]) < 2:
                cv = 0
                if ca > 0:
                    ca = ca-0.02
                else:
                    ca = 0
    
    dtau = controlador(y,ca,ch,cv)
    tau = (dtau +taun)*((dtau+taun)>0)
    
    #Fuerzas y pares ejercidos
    ut = np.dot(M,tau)
    #print(ut)
    SW = np.array([[0,-y[17],y[16]],[y[17],0,-y[15]],[-y[16],y[15],0]])
    R= y[6:15].reshape(3,3).T
    Rd=np.dot(R,SW)
    e3 = np.array([0,0,1])
    dy = np.array([\
                  g*e3-ut[0]*np.dot(R,e3)/m-b/m*y[0:3],\
                  y[0:3],\
                  Rd[:,0],Rd[:,1],Rd[:,2],\
                  -np.dot(Ji,np.dot(SW,np.dot(J,y[15:])))+np.dot(Ji,ut[1:])\
                    ]).reshape(18)
    
    return(dy)

def simulador(puntos, angulos):
    ''' esta función devuelve dos solver de scipy sol2 solo se ha construido 
    para depurar, el que usa el simulador es sol'''
    global cCartesianas
    global headings
    
    cCartesianas = puntos
    headings = angulos

    sol2 =RK45(lambda t,y:dt(t,y,taun,M,m,b,J,Ji),0.,y0,Tf,max_step=0.01)
    sol = solve_ivp(lambda t,y:dt(t,y,taun,M,m,b,J,Ji),\
          [0.,Tf],y0,t_eval=np.arange(0,Tf+0.1,0.1))

    return sol, sol2
    