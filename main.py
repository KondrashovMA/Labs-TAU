import numpy as np
import matplotlib.pyplot as plt
import control.matlab as ml
from sympy import *
import math
import scipy.integrate as integrate
import qualityInd
import CHRmeth as CHR

#исходные данные
k_u=21
T_g = 10 #секунд
T_u = 7 #секунд
T_nm = 7 #сек
k_nm = 3
k_oc = 0.1

k_u=23
T_g = 8 #секунд
T_u = 5 #секунд
T_nm = 5 #сек
k_nm = 1

#W_g = 1/(T_g*p + 1) генератор
#W_m = k_nm/(T_nm*p + 1) турбина
#W_u = k_u/(T_u*p+1) усилительно-исполнительный

w_g = ml.tf([1.], [8, 1]) #1
#w_m = ml.tf([0, 3], [0, 8.]) #2
w_m = ml.tf([3e-2, 1], [8e-2, 1.]) #2


w_u = ml.tf([21.], [7., 1.]) #3

#W_sumKnow = W_g*W_m*W_u
#w_g = ml.tf([1.], [10, 1]) #1
#w_m = ml.tf([1e-2, 1], [4e-1, 1.]) #2
#w_u = ml.tf([20.], [5., 1.]) #3
w_0=ml.tf([1],[1])

#w_g = ml.tf([4.], [10, 1]) #1
#w_m = ml.tf([6e-2,1], [0.035, 1]) #2
#w_u = ml.tf([24.], [5., 1.]) #3

print(w_g, w_m, w_u)

w_sumKnown = w_u*w_m*w_g

print("передаточная разомкнутая функция",w_sumKnown)


ww=w_sumKnown/(w_0+w_sumKnown)
y,x=ml.step(ww)
qualityInd.graph("Переходная функция замкнутой системы",y,x,"y","x","r")

print("передаточная замкнутая функция",ww)

y,x=ml.step(w_sumKnown)
qualityInd.graph("Переходная функция разомкнутой системы",y,x,"y","x","r")


print("Нахождение параметров регулирования методом CHR")
arrayPID = CHR.findingK(w_sumKnown,"PID")

timeReg = 15
coleb = 1.17
perereg = 22 # %
print("к-ты ",arrayPID) #  0 - просто, 1 - с 20% перерег., в каждом 0,1,2 - PID

