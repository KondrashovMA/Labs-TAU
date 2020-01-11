import random
import control.matlab as ml
from sympy import *
import matplotlib.pyplot as plt
import qualityInd
'''
class PID(): #класс PID Регулятора, в котором хранятся коэффициенты
    def __init__(self,P,I,D):
        self.P=P
        self.I=I
        self.D=D
    def getPID(self):
        array=[]
        array.append(self.P)
        array.append(self.I)
        array.append(self.D)
        return array
    def setPID(self,PID):
        self.P=PID[0]
        self.I=PID[1]
        self.D=PID[2]
'''
w_0=ml.tf([1],[1])

#w_g = ml.tf([1.], [8, 1]) #1
#w_m = ml.tf([0, 3], [0, 8.]) #2

#w_m = ml.tf([3e-2, 1], [8e-2, 1.]) #2
#w_u = ml.tf([21.], [7., 1.]) #3
#w_m = ml.tf([3e-2, 1], [8e-2, 1.]) #2

w_g = ml.tf([1.], [8, 1]) #1
#w_m = ml.tf([0, 3], [0, 8.]) #2
w_m = ml.tf([3e-2, 1], [8e-2, 1.]) #2


w_u = ml.tf([21.], [7., 1.]) #3

Try_number=100
New_try=50
Try_now=0
w_sumKnown = w_u*w_m*w_g


w=w_sumKnown/(w_0+w_sumKnown)
w_sumKnown = w_u*w_m*w_g
w=w_sumKnown/(w_0+w_sumKnown)
y,x=ml.step(w)
lim = y[-1]
print("уст. = ",lim)

plt.plot(x,y, label = "переходная объекта")
plt.grid(True)

plt.legend()
plt.show()




def generate_first_pop(): #50 особей, инициализация
    arrayPersons=[]
    for i in range(0,50):
        temp = []
        P=random.random()*100
        temp.append(P)
        I= random.random()*120
        temp.append(I)
        D=random.random()*50
        temp.append(D)

        arrayPersons.append(temp)
    return arrayPersons



def fitness(arrayPersons): #проверка на устойчивость и сравнение с желаемыми коэффициентами
    #arrayPersons массив особей, obj - объект управления, разомкнутая функция
    print("onstart ",len(arrayPersons))
    w_0=ml.tf([1],[1])
    errorValue=[]
    arraySortedPersons=[]

    obj = w_u*w_m*w_g

    for i in range(0, len(arrayPersons)):
        person = arrayPersons[i] # берём отдельную особь
        #array_of_PID=[]
        #array_of_PID = person.getPID()
        #print(person.getPID())
        rrr=[]



        #print(rrr, type(rrr))
        Kp = person[0] #P - 0 ,I - 1, D - 2
        Ki = person[1]
        Kd = person[2]

        #w_pid=ml.tf([Kd,Kp,Ki],[1.,1.])
        w_pid=ml.tf([Kd,Kp,Ki],[1.,1.])

        #w_pid=ml.tf([Kd,Kp,Ki],[1.,0.])

        w_with_reg = (obj*w_pid)/(w_0+obj*w_pid)  #w = w_sumKnown
        err=0
        y,x = ml.step(w_with_reg) #тк мы не должны опускаться ниже
        for i in range(len(y)):
            err += + (1-y[i])**2
        errorValue.append(err)

        #print("ошибка (точность ", err)

        arraySortedPersons.append(person)


        swapped = True #Устанавливаем swapped в True, чтобы цикл запустился хотя бы один раз
    while swapped:#сортируем ошибки по возрастанию, в начале самая большая
        swapped = False
        #print(len(errorValue)," ",len(arraySortedPersons))

        for i in range(len(errorValue) - 1):
            if errorValue[i] > errorValue[i + 1]:
                # Меняем элементы
                errorValue[i], errorValue[i + 1] = errorValue[i + 1], errorValue[i]
                arraySortedPersons[i],arraySortedPersons[i + 1] = arraySortedPersons[i + 1], arraySortedPersons[i]
                # Устанавливаем swapped в True для следующей итерации
                swapped = True

    testing(errorValue,arraySortedPersons)



def selection(arrayPersons):
    print("len на старте селекции ",len(arrayPersons))
    goodPersons = []
    #Селекция
    for i in range(0,10): #условно хорошие особи
        goodPersons.append(arrayPersons[i])
    #мутация
    for i in range(11,30):
        temp=[]
        P=random.random()*10
        temp.append(P)
        I= random.random()*100
        temp.append(I)
        D=random.random()*5
        temp.append(D)

        goodPersons.append(temp)

    # скрещивание
    fath = []
    math = []
    for i in range(10,31):
        fath.append(arrayPersons[i])
    #print("len fath",len(fath))
    for i in range (20,41):
        math.append(arrayPersons[i])
    #print("len math",len(math))
    #print(fath[12].getPID())
    temp=[]
    for i in range(0,len(fath)):
        num = random.randint(0,2) #случайно один из трёх признаков
        temp1 = fath[i]
        #print("temp1 ",temp1)
        temp2 = math[i]
        newAr = []
        for j in range(3):
            #print("j = ",j)
            if num==j:
                newAr.append(temp1[j]) #от первого
            else:
                newAr.append(temp2[j]) #от второго

        goodPersons.append(newAr)

    print("после селекции длина массива ",len(goodPersons))
    fitness(goodPersons)

goodOsb=[]
goodAndStableOsb=[]
bestOfbest=[]
notSoBest=[]
timeReg = 25 #15
coleb = 1.17#1.17
perereg = 22 #22 # %

def testing(errorValue,arraySortedPersons): # проверяем с переходной функцией, которую хотим получить
    #print(len(errorValue))
    print("тестинг, кол-во особей",len(arraySortedPersons))
    fl = False
    global timeReg
    global coleb
    global perereg
    global w_sumKnown
    global Try_number
    gotIt= False
    global Try_now
    for i in range(len(errorValue)):
        arr=arraySortedPersons[i]
        Kp=arr[0]
        Ki=arr[1]
        Kd=arr[2]

        w_pid=ml.tf([Kd,Kp,Ki],[1.,1.])
        #w_pid=ml.tf([Kd,Kp,Ki],[1.,0.])

        w_0=ml.tf([1],[1])
        w_with_reg = (w_pid*w)/(w_0+w_pid*w)
        y,x = ml.step(w_with_reg)
        plt.close()

        #print("errorValue[i] = ",errorValue[i])
        if(errorValue[i] < 1.05) and (y[-1]>lim*0.95) and (y[-1]<lim*1.05):
            if arraySortedPersons[i] not in goodOsb:
                goodOsb.append(arraySortedPersons[i])
        if(errorValue[i] < 1.05)and (qualityInd.stability(w_with_reg))and (y[-1]>lim*0.95) and (y[-1]<lim*1.05): #предельная ошибка
            if arraySortedPersons[i] not in goodAndStableOsb:
                goodAndStableOsb.append(arraySortedPersons[i])
            best = arraySortedPersons[i]
            #print("best = ", best.getPID())
            bestPID = best
            fl=0
            if (qualityInd.regTime(w_with_reg)<=timeReg):
                fl+=1
            if (qualityInd.coleb(w_with_reg)<=coleb):
                fl+=1
            if (qualityInd.perereg(w_with_reg)<=perereg):
                fl+=1
            #if(fl==2):
                #print("проходят по двум условиям")
                #print(bestPID)
                #notSoBest.append(bestPID)
            if(fl==3):
                print("very best = ", bestPID)
                if bestPID not in bestOfbest:
                    print("лучшие параметры регулятора:",bestPID)
                    bestOfbest.append(bestPID)
                    gotIt=False
                break
    Try_now = Try_now +1

    print("Try_now = ",Try_now)
    print("хорошие и устойчивые ",len(goodAndStableOsb))
    print("лучшие",len(bestOfbest))

    if(Try_now==Try_number):
        gotIt=True

    if(gotIt==False):
        selection(arraySortedPersons)


tst=[]
tst=generate_first_pop()

fitness(tst)
if(Try_now==New_try) and (len(bestOfbest)==0):
    tst=generate_first_pop()
    fitness(tst)
if(Try_now==Try_number and len(bestOfbest)!=0):
    k=1
    for elem in bestOfbest:
        Kp=elem[0]
        Ki=elem[1]
        Kd=elem[2]
        print("k"," вариант коэффициентов Kp = ",Kp," ; Ki = ",Ki," ; Kd = ",Kd)
        print("вывести график?")
        k = input()
        if(k=="y"):
            w_0=ml.tf([1],[1])
            w_sumKnown = w_u*w_m*w_g
            w=w_sumKnown/(w_0+w_sumKnown)

            w_pid=ml.tf([Kd,Kp,Ki],[1.,1.])
            #w_pid=ml.tf([Kd,Kp,Ki],[1.,0.])


            w_with_reg = (w_pid*w)/(w_0+w_pid*w)  #w = w_sumKnown

        #plt.close()
        #qualityInd.graph("Переходная",y,x,"","","r")
            t=range(0,200)
            yyTop=[]
            yyBot=[]
            y,x=ml.step(w_with_reg,t)
            plt.close()
            qualityInd.graph("Переходная с регулированием",y,x,"","","r")

            y,x=ml.step(w_with_reg,t)
            plt.plot(x,y, label="с регулятором")
            lastElem = y[-1]


            for elem in t:
                yyTop.append(lastElem*1.05)
                yyBot.append(lastElem*0.95)
            plt.plot(x,yyTop)
            plt.plot(x,yyBot)


            y,x=ml.step(w,t)
            plt.plot(x,y, label = "переходная объекта")
            plt.grid(True)

            plt.legend()
            plt.show()
            regTime = qualityInd.regTime(w_with_reg)

            coleb = qualityInd.coleb(w_with_reg)
            perereg = qualityInd.perereg(w_with_reg)
            fl = qualityInd.stability(w_with_reg)
            print("параметры системы")
            print("Устойчивость? ",fl)
            print("время рег ",regTime)
            print("колебательность",coleb)
            print("перерег.",perereg)
    for elem in goodAndStableOsb:
        Kp=elem[0]
        Ki=elem[1]
        Kd=elem[2]
        print("k"," вариант коэффициентов Kp = ",Kp," ; Ki = ",Ki," ; Kd = ",Kd)
