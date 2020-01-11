import control.matlab as ml
from sympy import *
import math
import qualityInd
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

regTypes={
    "PID": 0.6,
    "PI": 0.35,
    "P":0.3
}

def findingK(w,typeR):
    PID=[]
    PID_with_store=[]

    print("Для ",typeR," регулятора")

    y,x=ml.step(w)
    plt.close()

    tck = interpolate.splrep(x,y) #функция

    k=0
    for i in x:#поиск точки где касательная имеет наибольший угол (по тангенсу)
        if math.fabs(interpolate.splev(i,tck,der=1))>k:
            k=interpolate.splev(i,tck,der=1)
            maxX=i

    print("Тангенс ",k,"в точке",maxX )
    x0=11.25 #Вар ниже
    x0=12.1
    #x0=maxX
    #x0=4.5  #другая формула PID
    #x0=12.4 #для вар.А
    y0=interpolate.splev(x0,tck)
    dydx = interpolate.splev(x0,tck,der=1)

    tngnt = lambda x: dydx*x + (y0-dydx*x0) #формула касательной

    plt.plot(x,y,label = "Переходная хар-ка") #label - для легенды
    plt.plot(x0,y0, "or") #красный круг в точке х0 у0

    plt.plot(x,tngnt(x), label="Касательная") #по х и по лямбда-функции касательной в точке

    a=math.fabs(tngnt(x[0]))
    delt=0.5
    #mmn
    for i in np.arange(0,20,0.01):
        if math.fabs(tngnt(i))<delt:
            mmn = i
    print("более точное L",mmn)
    delt=0.9
    for i in x:
        if(math.fabs(tngnt(i))-0)<delt:
            delt = math.fabs(tngnt(i))
            findX=i

    L=findX
    #L=mmn
    print("a = ",a," L = ",L)

    plt.legend()
    plt.grid(True)
    plt.show()

    #без перерегулирования
    Kp=0.6/a
    Ti=1.0*L/Kp
    Ki=1/Ti
    Kd=0.5*L/Kp


    #с 20% запасом
    Kp_store=0.95/a
    Ti_store=1.4*L/Kp_store
    Ki_store=1/Ti_store
    Kd_store=0.47*L/Kp_store
    print("к-ты без перерегулирования")
    print("Kp = ",Kp,"\nKi = ",Ki,"\nKd = ",Kd)
    print("к-ты с 20%-перерегулированием")
    print("Kp = ",Kp_store,"\nKi = ",Ti_store,"\nKd = ",Kd_store)

    if(typeR=="PI"):
        Kd_store=0
        Kd=0

    if(typeR=="P"):
        Kd_store=0
        Kd=0
        Ki=0
        Ki_store=0

    w_pid=ml.tf([Kd,Kp,Ki],[1.,1.])
    #w_pid=ml.tf([Kd,Kp,Ki],[1.,0.])

    w_0=ml.tf([1],[1])

    w_with_reg = (w_pid*w)/(w_0+w_pid*w)  #w = w_sumKnown
    #w_with_reg = ml.feedback(w_pid*w,w_0,-1)




    print("передаточная функция регулятора", w_pid)
    print("передаточная функция с регулятором", w_with_reg)
    y,x=ml.step(w_with_reg)
    plt.close()
    qualityInd.graph("переходная функция с регулятором",y,x,"y","x","r")  #xmin, xmax, ymin, ymax


    w_pid_store=ml.tf([Kd_store,Kp_store,Ki_store],[1.,1.])
    #w_pid_store=ml.tf([Kd_store,Kp_store,Ki_store],[1.,0.])

    w_with_reg_store = (w*w_pid_store)/(w_0+w*w_pid_store)  #w = w_sumKnown
    y_store,x_store=ml.step(w_with_reg_store)
    plt.close()
    qualityInd.graph("переходная функция с регулятором  с запасом",y_store,x_store,"y","x","r")


    #w_full = w/(w_0+w)
    t=range(1,200)

    w_r=w/(w_0+w)
    y,x=ml.step(w_r,t)
    plt.plot(x,y, label = "переходная объекта")

    yyTop=[]
    yyBot=[]
    lastElem = y[-1]
    for elem in t:
            yyTop.append(lastElem*1.05)
            yyBot.append(lastElem*0.95)
    plt.plot(x,yyTop)
    plt.plot(x,yyBot)

    w_pid_hand=ml.tf([0.5,1,1.2],[1.,1.])
    #[Kd,Kp,Ki]

    w_0=ml.tf([1],[1])

    w_with_reg_hand = (w_pid_hand*w)/(w_0+w_pid_hand*w)

    y,x=ml.step(w_with_reg_hand,t)
    plt.plot(x,y, label = "переходная объекта с ручным регулированием")



    y,x=ml.step(w_with_reg,t)
    plt.plot(x,y, label="с регулятором")


    y,x=ml.step(w_with_reg,t)
    plt.plot(x,y, label="с регулятором")

    y,x=ml.step(w_with_reg_store,t)
    plt.plot(x,y, label="с регулятором с запасом")
    plt.grid(True)

    plt.legend()
    plt.show()
    final = []
    PID.append(Kp)
    PID.append(Ki)
    PID.append(Kd)
    PID_with_store.append(Kp_store)
    PID_with_store.append(Ki_store)
    PID_with_store.append(Kd_store)
    final.append(PID); final.append(PID_with_store)

    regTime = qualityInd.regTime(w_r)
    coleb = qualityInd.coleb(w_r)
    perereg = qualityInd.perereg(w_r)
    fl = qualityInd.stability(w_r)
    print("параметры системы")
    print("Устойчивость? ",fl)
    print("время рег ",regTime)
    print("колебательность",coleb)
    print("перерег.",perereg)

    regTime = qualityInd.regTime(w_with_reg)
    coleb = qualityInd.coleb(w_with_reg)
    perereg = qualityInd.perereg(w_with_reg)
    fl = qualityInd.stability(w_with_reg)
    print("параметры c регулятором")
    print("Устойчивость? ",fl)
    print("время рег ",regTime)
    print("колебательность",coleb)
    print("перерег.",perereg)

    regTime = qualityInd.regTime(w_with_reg_store)
    coleb = qualityInd.coleb(w_with_reg_store)
    perereg = qualityInd.perereg(w_with_reg_store)
    fl = qualityInd.stability(w_with_reg_store)
    print("параметры c регулятором с запасом")
    print("Устойчивость? ",fl)
    print("время рег ",regTime)
    print("колебательность",coleb)
    print("перерег.",perereg)
    return final











