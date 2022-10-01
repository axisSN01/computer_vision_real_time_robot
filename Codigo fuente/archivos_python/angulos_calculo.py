import math

def angulos_calculo(px,py):
    L0=9.5
    L1=8.5
    L2=10.5
    Lbase=6.5
    xmax=29
    xmin=5
    titamax=math.pi/2
    titamin=0

    if px==0.0:
        psi=math.pi/2
    else :
        psi=math.atan(py/px)
    x=math.sqrt(math.pow(px,2)+math.pow(py,2))
    y=1.5

    if x>=xmin and x<xmax:

        tita=x*(titamin-titamax)/(xmax-xmin)+titamin+xmax*(titamax-titamin)/(xmax-xmin)
        x1=x-math.cos(tita)*L2
        y1=y+math.sin(tita)*L2-Lbase
        alfa=math.asin((math.pow(x1,2)+math.pow(y1,2)+math.pow(L0,2)-math.pow(L1,2))/(2*L0*math.sqrt(math.pow(x1,2)+math.pow(y1,2))))-math.atan(-x1/y1)
        if alfa>0.1: alfa=math.pi-alfa
        elif alfa<0: alfa=-alfa
        fi=math.asin((-y1+math.sin(alfa)*L0)/L1)

        servo1=150-math.degrees(alfa)
        servo2=40+math.degrees(alfa+fi)
        servo3=90-math.degrees(tita-fi)

    if px>0.0:
        base=math.degrees(3.14-psi)
    else: 
        base=math.degrees(-psi)

    return (int(base),int(servo1),int(servo2),int(servo3))

def angulos_calculo_3d(px,py,pz):
    L0=9.5
    L1=8.5
    L2=10.5
    Lbase=6.5
    xmax=29
    xmin=5
    titamax=math.pi/2
    titamin=0

    if pz<3: pz=3

    psi = math.pi*px
    x = math.sqrt(math.pow(py,2)+math.pow(pz,2))
    alfa_elevacion = math.atan(pz/py)

    tita=x*(titamin-titamax)/(xmax-xmin)+titamin+xmax*(titamax-titamin)/(xmax-xmin)
    x1=x-math.cos(tita)*L2
    y1=2.5+math.sin(tita)*L2-Lbase
    alfa=math.asin((math.pow(x1,2)+math.pow(y1,2)+math.pow(L0,2)-math.pow(L1,2))/(2*L0*math.sqrt(math.pow(x1,2)+math.pow(y1,2))))-math.atan(-x1/y1)
    if alfa>0.1: alfa=math.pi-alfa
    elif alfa<0: alfa=-alfa
    fi=math.asin((-y1+math.sin(alfa)*L0)/L1)

    servo1=150-math.degrees(alfa+alfa_elevacion)
    servo2=40+math.degrees(alfa+fi)
    servo3=90-math.degrees(tita-fi)
    base=math.degrees(psi)

    return (int(base),int(servo1),int(servo2),int(servo3))

