import numpy as np
import matplotlib.pyplot as plt
import control.matlab as ml
from sympy import *
import math
import qualityInd
import scipy.integrate as integrate
def trapezoidal(f, a, b, n): # честно взято из интернета
	"""
	Вычисляет приближенное значение интеграла с помощью формулы трапеций
	f - подынтегральная функция
	a, b - пределы интегрирования
	n - количество частичных отрезков
	"""
	h = float(b - a)/n
	result = 0.5*(f(a) + f(b))
	for i in range(1, n):
		result += f(a + i*h)
	result *= h
	return result

#исходные данные
k_u=23
T_g = 10 #секунд
T_u = 7 #секунд
#T_gt нет
T_nm = 7 #сек
k_nm = 3
#T_oc нет

#W_g = 1/(T_g*p + 1)
#W_m = k_nm/(T_nm*p + 1)
#W_u = k_u/(T_u*p+1)

#w_reg - искомое

#W_sum = W_g*W_m*W_u

#w_g = ml.tf([0, 1], [T_g, 1]) #1
#print(w_g)
#w_m = ml.tf([k_nm], [T_nm, 1]) #2
#print(w_m)
#w_u = ml.tf([k_u], [T_u, 1]) #3

w_g = ml.tf([1.], [8, 1]) #1
#w_m = ml.tf([0, 3], [0, 7.]) #2

w_m = ml.tf([0, 3], [0, 7.]) #2

w_u = ml.tf([21.], [7., 1.]) #3
#print(w_u)
#_________________w_reg = ml.tg()

w_sumKnown = w_g*w_m*w_u #последовательное соединение известных значений 
#print(w_sum)

delta = 0.23 #перерегулирование деленное на 100%
t_reg = 14 #время после которого переходная функция не выходит за диапазон
M=1.18

#w_pid=ml.tf([k_p], [1]) + ml.tf([0, k_i], [1, 0]) + ml.tf([k_d, 0], [0,1])
def enter(name, *txt):
    k=None
    while k==None: 
        print("ввод ",name,*txt)
        try:
            k = input()
            if k=="n":
                return None
            else:
                k=float(k)
        except ValueError:
            print("Ввести нужно число")
            k=None
    return k
k_p=k_i=k_d=0    
while True:
    k_p = enter("k_p", "если ввести n то программа остановится")
    if(k_p==None): break
    k_i = enter("k_i")
    if(k_i==None):break
    k_d = enter("k_d")
    if(k_d==None):break

    # ПИД W pid = Kp + Ki/p + Kd*p
    w_pid=ml.tf([k_p], [1]) + ml.tf([0, k_i], [1, 0]) + ml.tf([k_d, 0], [0,1])

    w_pid=ml.tf([k_d,k_p,k_i],[1.,1.])
    # ПИ Wpi = Kp + Ki/p
    #w_pi = ml.tf([k_p], [1]) + ml.tf([0, k_i], [1, 0])
    print("передаточная регулятора", w_pid) #тут менять


    w_sum = w_pid*w_sumKnown  #тут менять
    w = ml.feedback(1,w_sum) # передаточная функция
    w = w_sum/(1+w_sum)

    w_zam = w_sumKnown/(1+w_sumKnown)


    y,x = ml.step(w_zam)
    plt.plot(x,y, label="переходная системы")


    y,x=ml.step(w)
    plt.plot(x,y, label="переходная системы c регулированием")
    plt.grid(True)

    plt.legend()
    plt.show()

    print("Передаточная функция системы без регулятора: ", w_sumKnown)
    print("Передаточная функция системы: ", w)
    print("Передаточная функция разомкнутной системы: ", w_sum)
    
    def graph(name,y, x, ylabel, xlabel, color, *ax):
        plt.plot(x,y,color)
        plt.title(name)
        plt.grid(True)
        plt.axis(*ax) #xmin, xmax, ymin, ymax
        plt.show()
#_______________________________________________________________________________________________________________

    print("Прямые оценки качества:")
    t=range(1,1000)         
    #Переходная 
    y,x=ml.step(w)
    plt.close()

    lastElem = y[-1]
    preLastElem = y[-2]
    yyTop=[]
    yyBot=[]
    fl=True

    if (lastElem/preLastElem>=0.9 or lastElem/preLastElem<=1.1):
        for i in range(1,10):
            if (lastElem/y[-i]<=0.9 or lastElem/y[-i]>=1.1): #если хотя бы 10 последних элементов примерно в одном диапазоне, считаем, что функция пришла к уст. значению
                fl=False
        if(fl):
            for elem in x:
                yyTop.append(lastElem*1.05)
                yyBot.append(lastElem*0.95)
            plt.plot(x,yyTop)
            plt.plot(x,yyBot)
            print("крайние ",lastElem)

            #Время регулирования по переходной функции

            for k in range(len(y)):
                #print(lastElem*1.05," ",lastElem*0.95," ",y[-k])
                if((y[-k] > lastElem*1.05 or y[-k] < lastElem*0.95) and y[-k]!=0) : # идём с конца массива и ищем точку пересечения с прямыми +- 5%
                    print(lastElem*1.05," ",lastElem*0.95," ",y[-k])
                    ind=k
                    break
            ind = len(x)-ind
            #print("Точка пересечения с +-5 % ",x[ind])
            print("время регулирования: ",x[ind])
        else:
            print("система расходится, время регулирования не определить")
        
    #print("отношение последнего к предпоследнему",y[-1]/y[-2])
    graph("Переходная функция", y, x, "Amplitude", "Time", "b")

#_______________________________________________________________________________________________________________

    w_den = ml.tf(w.den[0][0], [1])
    crt=ml.pzmap(w_den)
    plt.close()
    #если берем от знаменателя - а от него берём чтобы считать только полюса, нужно [1]
    first_elem=crt[1]
    print("Значения полюсов передаточной функции:")
    minim=[]
    for ans in first_elem:
        print("анс ту____________________________________________т")
        print(ans)
        print(re(ans))
        min_ans=re(first_elem[0])
        minim.append(first_elem[0])
        for i in range(1, len(first_elem)):
            if math.fabs(re(first_elem[i])) < math.fabs(min_ans):
                minim=[]
                minim.append(first_elem[i])
                min_ans = re(first_elem[i])
            elif re(first_elem[i])==min_ans:
                minim.append(first_elem[i])
    #print("minim", minim)
    t_reg = math.fabs(3/re(minim[0]))
    print("max = ", max(y))
    delt=(max(y)-y[-1])/y[-1]*100
    print("Перерегулирование: ", delt," %")
    yy=[]
    xx=[]
    for elem in y:
        yy.append(elem)
    for elem in x:
        xx.append(elem)
        
    ind = yy.index(max(yy))#индекс первого максимума
    first_max = max(yy)
    copy_yy=[]
    copy_yy=yy #создаём копию массива, удаляем из неё сначала первый, затем второй максимумы. соответственно, оставшиеся это второй и третий.
    copy_yy.remove(first_max)
    
    second_max = max(copy_yy)#второй максимум собственно
    ind_sec = copy_yy.index(second_max)
    copy_yy.remove(second_max)
    third_max = max(copy_yy)

    colb = first_max/second_max
    print("Колебательность как отношение первого и второго максимумов : ",colb)

    st_y = 1-first_max/third_max
    print("Степень затухания: ", st_y)

    print("Величина и время достижения первого max, max= : ",first_max ," t= ", xx[ind])
    print()
    #_________________________________________________________________________________________________________________
    print("По распределению корней:")
    crt=ml.pzmap(w_den)
    plt.grid(True)
    plt.show()
    print("время регулирования: ", t_reg)
    
    maxm=[]
    max_ans=re(first_elem[0])
    maxm.append(first_elem[0])
    for i in range(1, len(first_elem)):
        if (im(first_elem[i])!=0):
            if math.fabs(re(first_elem[i])) > math.fabs(max_ans):
                maxm=[]
                maxm.append(first_elem[i])
                max_ans = re(first_elem[i])
            elif re(first_elem[i])==max_ans:
                maxm.append(first_elem[i])
    mu = math.fabs( im(maxm[0])/re(maxm[0]) )
    print("Степень колебательности ", mu)
    if(mu!=0):
        print("Тогда перерегулирование сигма< ",math.exp(math.pi/mu))
        psi = 1 - math.exp(-2*math.pi/mu)
        print("Степень затухания: ",psi)
    else:
        print("Степень колебательности = 0, нельзя определить перерегулирование и степень затухания")
    print()
    #________________________________________________________________________________________________________________
    print("Показатели качества по ЛЧХ")
    #mag, phase, omega = ml.bode(w, dB=True) #от замкнутной
    mag, phase, omega = ml.bode(w, dB=False) #от разомкнутой
    plt.show()
    #plt.close()

    M = max(mag)/mag[0]
    print("Показатель колебательности ", M )

    k=0
    start=round(mag[0],2)
    #print(mag)
    mag, phase, omega = ml.bode(w, dB=False)
    plt.close()
    for i in range(len(omega)-2):
        if (round(mag[i+1],2)==start and round(mag[i+1],2)!=round(mag[i+2],2)): #ищем вторую точку пересечения с A(0), проверяем, что не равна сразу следующей
            ind = i+1
            break
        
    print("Индекс конца ", ind)   
    print("Время регулирования: ", 1.5*2*math.pi/omega[ind])

    mag, phase, omega = ml.bode(w, dB=True) #от разомкнутой
    #plt.close()
    plt.show()

    ph=[]
    for item in phase:
        ph.append(round(item*180/math.pi,3))
    dif=1.2
    fl=False
    index = 0
    for item in ph:
        if item<0:
            if dif>math.fabs(180-math.fabs(item)): #ищем самое близкое к 180 число
                fl=True
                dif = math.fabs(180-math.fabs(item))
                index = ph.index(item) # в массиве номер ближайшего к 180, для нахождения точки пересечения
                f=item
    if(fl==False):
        print("Нет нужных пересечений, нет запаса по амплитуде")
    else:
        print("самое близкое к 180 ",f, "разница ",dif," индекс ",index)
        amp=1-mag[index]
        print("Значение запаса по амплитуде в этой точке: ",amp) #считаем запас от A(w)=1

    dif=0.001
    fl=False
    index = 0
    #print(mag)
    ampl = []

    for item in mag:
        ampl.append(item)

    for item in mag:
        if dif>math.fabs(0-math.fabs(item)): #ищем самое близкое к 180 число
            fl=True
            dif = math.fabs(1-math.fabs(item))
            index = ampl.index(item)
    if(fl==False):
        print("Нет нужных пересечений, нет запаса по фазе")
    else:
        print( "разница ",dif," индекс ",index)
        phz=math.fabs(180)-math.fabs(ph[index])
        print("Значение запаса по фазе в этой точке: ",phz) #считаем запас от A(w)=1
    
#________________________________________________________________________________________________________________

    print("линейная интегральная оценка")

    pos_inf = float('inf')
    #print("*" * 20, "\n"
    #"Интеграл составил: ", integro)
    print(" w by inf ",w(pos_inf))
    print("inf ",pos_inf)
    print(lastElem)
    I = trapezoidal((lastElem-w), 0, t_reg, 50)
    print(I)




    print("было: ","k_p",k_p,"k_i",k_i,"k_d",k_d)




