import matplotlib.pyplot as plt
import control.matlab as ml
from sympy import *
import math
def graph(name,y, x, ylabel, xlabel, color, *ax):
        """
	    Строит график функции
	    """
        plt.plot(x,y,color)
        plt.title(name)
        plt.grid(True)
        plt.axis(*ax) #xmin, xmax, ymin, ymax
        plt.show()


def proz(w,x):
        deltaX=1E-9
        pr=( w(x+deltaX)-w(x-deltaX) )/(2*deltaX)
        return pr

def stability(w):
        w_den = ml.tf(w.den[0][0], [1])
        plt.close()
        crt=ml.pzmap(w_den)
        plt.close()
        first_elem=crt[1]
        isIt=True
        for ans in first_elem:
                min_ans=re(first_elem[0])
                if min_ans>0:
                        isIt = False
        return isIt

def regTime(w): #время регулирования
        w_den = ml.tf(w.den[0][0], [1])
        crt=ml.pzmap(w_den)
        plt.close()
        #если берем от знаменателя - а от него берём чтобы считать только полюса, нужно [1]
        first_elem=crt[1]
        minim=[]
        for ans in first_elem:
                min_ans=re(first_elem[0])
                minim.append(first_elem[0])
                for i in range(1, len(first_elem)):
                    if math.fabs(re(first_elem[i])) < math.fabs(min_ans):
                        minim=[]
                        minim.append(first_elem[i])
                        min_ans = re(first_elem[i])
                    elif re(first_elem[i])==min_ans:
                        minim.append(first_elem[i])
        #print("re = ",re(minim[0]))
        dop = re(minim[0])*10
        if (dop==0):
                t_reg=999999
        else:
                t_reg = math.fabs(3/re(minim[0]))
        return t_reg

def coleb(w): #колебательность
        y,x=ml.step(w)
        plt.close()
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
        #print("Колебательность как отношение первого и второго максимумов : ",colb)
        return colb



def perereg(w):
        y,x=ml.step(w)
        plt.close()
        delt=(max(y)-y[-1])/y[-1]*100
        return delt

