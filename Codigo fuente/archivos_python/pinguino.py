#! /usr/bin/python
#-*- coding: utf-8 -*-

import serial,os,time,sys
from time import sleep as delay
from PyQt4 import QtCore, QtGui
from angulos_calculo import *

class pinguino(QtCore.QThread):
    def __init__(self, dic, parent = None):
        QtCore.QThread.__init__(self)
        self.puerto=''
        self.dic=dic

#-----------------------------------------------------------
    def destino_XY(self,lista):
        """intenta inferenciar la posicion del objeto en base a su movimiento.MRU"""
       # print "puntos:", lista
       # print "\n t_frames: ", self.dic["t_frames"]
       # print "\n t_busqueda: ", self.dic["t_busqueda"]        
        x0=float(lista[0])
        y0=float(lista[1])
        xf=float(lista[len(lista)-2])
        yf=float(lista[len(lista)-1])
        dX=xf-x0    # delta de x
        dY=yf-y0    # delta de y
        # x a continuacion inferencio x+1
        x = dX/self.dic["t_frames"]*float(self.dic["t_busqueda"]) + x0 #   x= dX/t * T + x0
        # ahora obtengo y +1
        y = dY/dX*(x-x0) + y0
        print "\n X e Y: ", x, y      
        return int(x), int(y) 
        
#-----------------------------------------------------------

    def prom(self,lista,z):
        """ Calcula el promedio del centro de tracking por indice, prom(lista,indice) """
        sum=0.0
        if (z=='x'):
            for i in range(0,len(lista),2):
	            sum=sum+lista[i]
        elif z=='y':
            for i in range(1,len(lista),2):
	            sum=sum+lista[i]
        return 2*sum/len(lista)   # si la lista es impar devuelve un numero flotante aproximado.

#-----------------------------------------------------------

    def RecursiveConect(self,max_puertos=20):
        """ Se conecta automáticamente con el primer pinguino que encuentre habilitado """
        cont=0
        while cont<=max_puertos: 
            try:
                if os.name=='posix':
                    if self.Conect('/dev/ttyACM'+str(cont)):
			self.emit(QtCore.SIGNAL('conectado'))
			return True
		elif os.name=='nt':
                    if self.Conect('COM'+str(cont)):
			self.emit(QtCore.SIGNAL('conectado'))
                        return True
            except: pass
            cont+=1         
        return False 
 
#-----------------------------------------------------------

    def Conect(self,puerto):
        """ Inicializa la comunicación """
        try:
            self.ping=serial.Serial(puerto,115200,timeout=0.2)
            delay(1)
            self.ping.write("co")
            if self.ping.read(10)=="conectados":
                self.puerto=puerto
                return True
        except: pass

#-----------------------------------------------------------
        
    def close(self):
        """ Finaliza la comunicación """
        try:
            self.ping.close()
        except: pass
#-----------------------------------------------------------
    def run(self):
        while True:
            if self.puerto=='':
                if not self.RecursiveConect(): 
                    self.emit(QtCore.SIGNAL('errorconexion'))
                    return
            if self.dic["buscar"]:
                self.ping.flushInput()
                self.busqueda()
#-----------------------------------------------------------
    def busqueda(self):
        self.centro=self.dic["centro"]
        self.xmin = self.dic["rectangulo"][0]     # tamaño y posicion en px del rect de trabajo
        self.ymin = self.dic["rectangulo"][1]    
        self.xmax = self.dic["rectangulo"][2]
        self.ymax = self.dic["rectangulo"][3]
        self.pxTocm=self.dic["lineablanca"]/40.0
        i=0
        flag=0
        x=0
        try:
            self.centro_obj_x, self.centro_obj_y=self.destino_XY(self.centro)
            self.dic["destino"]=(self.centro_obj_x,self.centro_obj_y)  # destino se usa en aplicaicon1.py, para dibujar un circulo a donde debe ir
            self.pos_cm_x=self.pxTocm*((self.xmax-self.xmin)/2-self.centro_obj_x)
            self.pos_cm_y=self.pxTocm*(self.centro_obj_y-self.ymin)
        except:
            self.dic["destino"]=(0,0)
            self.dic["buscar"]=False
            self.dic["centro"]=[]
            return
        try:
            if self.centro_obj_x<self.xmax and self.centro_obj_x>self.xmin and self.centro_obj_y<self.ymax and self.centro_obj_y>self.ymin:
                (self.servobase,self.servo1,self.servo2,self.servo3)=angulos_calculo(self.pos_cm_x,self.pos_cm_y)
                self.z1=str(self.servo1).zfill(3)        
                self.z2=str(self.servo2).zfill(3)
                self.z3=str(self.servo3).zfill(3)
                self.ba=str(self.servobase).zfill(3)
            else:
                self.emit(QtCore.SIGNAL('objetofuera'))
                self.dic["buscar"]=False
                self.dic["centro"]=[]
                return
        except:
            self.emit(QtCore.SIGNAL('objetofuera'))
            self.dic["buscar"]=False
            self.dic["centro"]=[]
            return
        # caculo de x e y en grados del servo base, supongo 180 grados de BW:
        # envio orden  a pinguino
        i=1
        while(i):
            try:
                self.ping.write('bu')
                if self.ping.read(5)=='busco':
                    i=0
                    self.ping.write(self.z1)
                    self.ping.write(self.z2)
                    self.ping.write(self.z3)
                    self.ping.write(self.ba)
            except:
                self.emit(QtCore.SIGNAL('errorconexion'))
                self.dic["buscar"]=False
                self.dic["centro"]=[]
                return

        try:
            self.ping.read(8)
        except:
            self.emit(QtCore.SIGNAL('nocontesta'))
            self.dic["buscar"]=False
            self.dic["centro"]=[]
            return
        self.emit(QtCore.SIGNAL('buscando'))
        delay(4)
        self.dic["buscar"]=False
        self.dic["centro"]=[]
        delay(1)
        return

