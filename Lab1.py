import numpy as np
#import control.matlab as ml
import matplotlib.pyplot as plt
import control.matlab as ml


timeVector = np.array([0,20])
def create_Plot(var,name,num, den):
    W=ml.tf(num,den)
    if var!=5:
        #Переходная функция
        plt.figure().canvas.set_window_title(name)
        y,x=ml.step(W,timeVector)
        plt.plot(x,y,"b")
        plt.title('Переходная функция')
        plt.ylabel('Амплитуда, о.е.')
        plt.xlabel('Время, с.')
        plt.grid(True)
        #TimeLine=[]
        #for i in range(0;3000):
        #   TimeLine = [i/1000]
        plt.show()
            #Импульсная функция
        plt.figure().canvas.set_window_title(name)
        y,x=ml.impulse(W,  timeVector)
        plt.plot(x,y,"r")
        plt.title('Импульсная функция')
        plt.ylabel('Амплитуда, о.е.')
        plt.xlabel('Время, с.')
        plt.grid(True)
        plt.show()
    #Диаграмма Боде
    plt.figure().canvas.set_window_title(name)
    mag, phase, omega = ml.bode(W, dB=False)
    plt.plot()
    plt.xlabel('Частота, Гц')
    plt.show()
    return

varia={'Безынерционное': 1, 'Апериодическое': 2, 'Интегрирующее':3,
       'Реальное дифф':4, 'Идеальное дифф':5, 'Выход':6}

while True:
    sorted_dict = sorted(varia.items(), key=lambda kv: kv[1])
    print('Введите нужное дейтсвие')
    for i in sorted_dict:
        print(i[0],' - ', i[1])
    var=int(input())
    if var not in [i for i in range(7)]:
        print('Некорректный ввод')
    elif var==6:
        break
    elif var==1:
        num=[4.]
        den=[1.]
        name="Безынерционное"
        create_Plot(var,name, num, den)
    elif var==2:
        num=[5.]
        den=[3., 1]
        name='Апериодическое'
        create_Plot(var,name, num, den)
    elif var==3:
        num=[3.]
        den=[1.,0.]
        name='Интегрирующее'
        create_Plot(var,name, num, den)
    elif var==4:
        num=[3.,0.]
        den=[5.,1.]
        name='Реальное дифф'
        create_Plot(var,name, num, den)
    elif var==5:
        num=[1.,0]
        #den [1*10**(-6)., 1] должно решить проблемы
        den=[0.,1]
        name='Идеальное дифф'
        create_Plot(var,name, num, den)