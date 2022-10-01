#!/usr/bin/python -d
#-*- coding: utf-8 -*-
 
import sys, numpy
from PyQt4 import QtCore, QtGui
from archivos_python import *
from archivos_python.ventana_principal1 import Ui_ventana
from archivos_python.multiples_objetos import *
from archivos_python.pinguino import *
from ConfigParser import RawConfigParser
import cv, pdb
import time
import aplicacion2

# diccionario global de variables y para debug
dic={"centro":[],"rectangulo":[0,0,0,0],"lineablanca":2.5,"buscar":False, "is_disp":False,"cuenta":0,"t_frames":0,"t_busqueda":0,
     "crit":0,"t_min":2.5,"t_max":5.0,"hist":[50,100,255,255],"Erode":0,"Dilate":0,"destino":(0,0)}

#notas:
# t_min y t_max estan en cm2
#lineablanca esta en cm, pinguino tiene q multiplicar por 40.0

class Aplicacion(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ventana()
        self.ui.setupUi(self)
        try:
            self.capture = cv.CreateCameraCapture(-1)
            cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_BRIGHTNESS,0.5)
        except:
            self.ui.consola.append(">>>Imposible leer camara (reinicie)\n") 
        self.frame=None
        self._frame = None
        self.selection=(0, 0, 0, 0)
        self.hist_map=(100,100,100,100)
        self.posicion=None
        self.inicio_arrastre=None
        self.drag_start = None
        self.track_window = (0, 0, 0, 0)
        self.tupla=(300,600)
        self.segundos=10
        self.cont=0
        self.range_list=(0,0,0,0)
        global dic
        self.dic=dic
        self.ui.groupBox_conf.setEnabled(False)
        self.ui.groupBox_probar.setEnabled(False)
        
        self.ui.pushButton_conf.clicked.connect(self.calibrar)
        self.ui.pushButton_probar.clicked.connect(self.probar)        
        self.ui.pushButton_iniciar.clicked.connect(self.iniciar)
        self.ui.actionCerrar.triggered.connect(self.cerrar)
        self.ui.actionAcerca.triggered.connect(self.acerca)
        self.ui.actionInstrucciones.triggered.connect(self.instrucciones)
        self.ui.actionContacto.triggered.connect(self.contacto)
        self.ui.actionCargar.triggered.connect(self.cargar_configuracion)
        self.ui.actionGuardar.triggered.connect(self.guardar_configuracion)
        self.ui.actionAp2.triggered.connect(self.iraplicacion2)
        #self.hist = cv.CreateHist([180], cv.CV_HIST_ARRAY, [(0,180)], 1 )
        self.hist = cv.CreateHist([255], cv.CV_HIST_ARRAY, [(0,254)], 1 )        
        self.cargar_configuracion()                             #cargo configuracion inicial
        self.conectar()                        #inicializo comunicacion con arduino
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.mostrar)
        self._timer.start(10)
        self.center()

#-----------------------------------------------------------------------------

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

#-----------------------------------------------------------------------------

    def cargar_configuracion(self):
        try:
    #--------------------------------leo .conf---------------------------------------
            self.ui.consola.append(">>>Cargando configuracion\n")
            self.config=RawConfigParser()
            archivo=open(sys.path[0]+'/config/config_app1.conf','r')
            self.config.readfp(archivo)
            self.dic["lineablanca"]=float(self.config.get("linea","tamano"))  # divido por tamaño ñinea blanca 40px
            self.dic["rectangulo"][0]=int(self.config.get("rectangulo","rectangulo0"))
            self.dic["rectangulo"][1]=int(self.config.get("rectangulo","rectangulo1"))
            self.dic["rectangulo"][2]=int(self.config.get("rectangulo","rectangulo2"))
            self.dic["rectangulo"][3]=int(self.config.get("rectangulo","rectangulo3"))
            self.dic["crit"]=int(self.config.get("criterio","criterio"))
            self.dic["t_busqueda"]=int(self.config.get("criterio","t_busqueda"))
            self.dic["cuenta"]=int(self.config.get("criterio","cuenta"))
            self.dic["Erode"]=int(self.config.get("criterio","Erode"))
            self.dic["Dilate"]=int(self.config.get("criterio","Dilate"))
            self.dic["t_min"]=float(self.config.get("tamano","minimo"))
            self.dic["t_max"]=float(self.config.get("tamano","maximo"))
            self.dic["hist"]=[int(self.config.get("hist","x_min")),int(self.config.get("hist","x_max")),int(self.config.get("hist","v_min")),int(self.config.get("hist","v_max"))]
            archivo.close()

    #--------------------------------algoritmo cargar histograma---------------------------------------
            for i in range(0,254):              # presupongo mi histograma de 180 bins. ahora presupongo 255
                if i<=self.dic["hist"][0]:       # mientras sea menor q x_min es =0
                    self.hist.bins[i]=0
                if i>self.dic["hist"][0] and i<=self.dic["hist"][1]:  self.hist.bins[i]=255
                if i>self.dic["hist"][1]: 
                    self.hist.bins[i]=0

            self.ui.consola.append(">>>Configuracion cargada con exito!!\r\n")  
        except:
            self.ui.consola.append(">>>Problemas leyendo archivo .conf !!\r\n")
       
        self.ui.doubleSpinBox_px2cm.setValue(self.dic["lineablanca"])
        self.ui.comboBox_size.setCurrentIndex(self.dic["crit"])
        self.ui.doubleSpinBox_cmMin.setValue(self.dic["t_min"])
        self.ui.doubleSpinBox_cmMax.setValue(self.dic["t_max"])
        self.ui.slider_Erode.setValue(self.dic["Erode"])
        self.ui.slider_Dilate.setValue(self.dic["Dilate"])
        self.ui.slider_interp.setValue(self.dic["cuenta"])

#--------------------------------set tab iniciar---------------------------------------
        self.ui.label_config.clear()
        self.ui.label_config.setText("Rectangulo: "+str(self.dic["rectangulo"])+"\n"+
                                      "Criterio: "+str(self.ui.comboBox_size.currentText())+"\n"+  # texto de cada ind.
                                        "Tamano: "+str(self.dic["t_min"])+" a "+str(self.dic["t_max"])+"cm2\n"+
                                        "Histograma: "+str(self.dic["hist"])+"\n"+
                                       "Linea blanca: "+str(self.dic["lineablanca"])+"\n"+
                                         "Interpolacion (N frames): "+str(self.dic["cuenta"]))
    
#----------------------------------------------------------------------

    def guardar_configuracion(self):
        self.config=RawConfigParser()
        archivo=open(sys.path[0]+'/config/config_app1.conf','r')
        self.config.readfp(archivo)

        self.config.set("linea","tamano",self.dic["lineablanca"])
        self.config.set("rectangulo","rectangulo0",self.dic["rectangulo"][0])
        self.config.set("rectangulo","rectangulo1",self.dic["rectangulo"][1])
        self.config.set("rectangulo","rectangulo2",self.dic["rectangulo"][2])
        self.config.set("rectangulo","rectangulo3",self.dic["rectangulo"][3])
        self.config.set("criterio","criterio",self.dic["crit"])
        self.config.set("criterio","cuenta",self.dic["cuenta"])
        self.config.set("criterio","Erode",self.dic["Erode"])
        self.config.set("criterio","Dilate",self.dic["Dilate"])
        self.config.set("tamano","minimo",self.dic["t_min"])
        self.config.set("tamano","maximo",self.dic["t_max"])
        self.config.set("hist","x_min",self.dic["hist"][0])
        self.config.set("hist","x_max",self.dic["hist"][1])   # v_min y v_max de 255, asi me queda una ventana cuadrada

        archivo=open(sys.path[0]+'/config/config_app1.conf',"w")
        self.config.write(archivo)
        self.ui.consola.append(">>>Configuracion guardada!! "+time.strftime("%a, %d/%b/%y, %H:%M:%S",time.gmtime())+"\n")       
        archivo.close()

#-----------------------------------------------------------------------------

    def mousePressEvent(self,event):
        """Evento para el click del mouse"""
        if self.ui.pushButton_conf.isChecked() or self.ui.pushButton_dib_hist.isChecked():
            self.posicion = self.ui.labelcamara.mapFromGlobal(QtGui.QCursor.pos())
            self.inicio_arrastre = (self.posicion.x(),self.posicion.y())
 
    def mouseReleaseEvent(self,event):
        """Evento para el release del mouse"""
        self.inicio_arrastre = None
        self.track_window = self.selection

    def mouseMoveEvent(self, event):
        """Evento para el movimiento del mouse"""
        if self.inicio_arrastre and self.ui.pushButton_conf.isChecked() or self.ui.pushButton_dib_hist.isChecked():
            self.posicion = self.ui.labelcamara.mapFromGlobal(QtGui.QCursor.pos())  
            xmin = min(self.posicion.x(), self.inicio_arrastre[0])
            ymin = min(self.posicion.y(), self.inicio_arrastre[1])
            xmax = max(self.posicion.x(), self.inicio_arrastre[0])
            ymax = max(self.posicion.y(), self.inicio_arrastre[1])
            self.selection = (xmin, ymin, xmax, ymax)
            if self.ui.pushButton_conf.isChecked() and not self.ui.pushButton_dib_hist.isChecked():# si estoy configurando y no estoy en hist
                self.dic["rectangulo"]=[self.selection[0],self.selection[1],self.selection[2],self.selection[3]]
            else: self.hist_map=(xmin, ymin, xmax - xmin, ymax - ymin)              # caso contrario estoy en hist 

#-----------------------------------------------------------------------------

    def build_image(self, frame):
        """ Transforma iplimages a qimages """
        if not self._frame:
            self._frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(frame, self._frame)
        else:
            cv.Flip(frame, self._frame, 0)
        return IplQImage(self._frame)

#-----------------------------------------------------------------------------

    def mostrar(self):
        self.frame = cv.QueryFrame(self.capture)
        try:
#--------------------siempre dibujo el cuadro azul---------------------------------------------------------
            cv.Rectangle(self.frame, (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]-int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]),
                                         (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]+int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]+int(320/self.dic["lineablanca"])),[255,0,0],1,8, 0)  # rectangulo de posicion del brazo
                
            cv.Rectangle(self.frame, (self.dic["rectangulo"][0],self.dic["rectangulo"][1]), (self.dic["rectangulo"][2],self.dic["rectangulo"][3]),[255,0,0],1,8, 0)
            cv.Line(self.frame, (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]-10), (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]+10), [25,20,175], thickness=2, lineType=cv.CV_AA, shift=0)

        except: self.ui.consola.setText(">>>Problema en mostrar!!")
        self.image = self.build_image(self.frame)
        self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))

#-----------------------------------------------------------------------------

    def hue_histogram_as_image(self, hist):
        """ Devuelve la iplimage del histograma """
        histimg_hsv = cv.CreateImage( (380,80), cv.IPL_DEPTH_8U, 3)
        mybins = cv.CloneMatND(hist.bins)
        cv.Log(mybins, mybins)
        (_, hi, _, _) = cv.MinMaxLoc(mybins)
        cv.ConvertScale(mybins, mybins, 255. / hi)
        w,h = cv.GetSize(histimg_hsv)
        hdims = cv.GetDims(mybins)[0]
        for x in range(w):
            xh = (180 * x) /(w - 1) 
            if mybins[int(180 * x / w)]>0: val = int(mybins[int(180 * x / w)] * h / 255)
            else: val=0
            cv.Rectangle( histimg_hsv, (x, 0), (x, h-val), (xh,255,64), -1)
            cv.Rectangle( histimg_hsv, (x, h-val), (x, h), (xh,255,255), -1)
        histimg = cv.CreateImage( (w,h), cv.IPL_DEPTH_8U, 3)
        cv.CvtColor(histimg_hsv, histimg, cv.CV_HSV2BGR)
        return histimg

#-----------------------------------------------------------------------------
    def probar(self):
        if not self.ui.pushButton_conf.isChecked() and self.ui.pushButton_probar.isChecked():
            self.ui.menubar.setEnabled(False)  # desactivo barra de menu
            self.ui.pushButton_conf.setEnabled(False)# desactivo conf
            self.ui.groupBox_conf.setEnabled(False)
            self.ui.tabWidget.setTabEnabled(0, False)  # anulo tab uno hasta q toggle boton conf            
            self.ui.groupBox_probar.setEnabled(True)# activo grupo probar, por las dudas    
            self.ui.pushButton_probar.setText("Aceptar")
            self._timer.stop()
            self.cont=0
            #----------algoritmos de buqueda--------------------------------------------------------------
            while self.ui.pushButton_probar.isChecked():
                self.dic['cuenta']=self.ui.slider_interp.value() #renuevo el diccionario
                self.dic['Erode']=self.ui.slider_Erode.value()
                self.dic['Dilate']=self.ui.slider_Dilate.value()
                self.ui.label_interp.setText("Interpolacion: "+str(self.dic['cuenta']))
                self.ui.label_Erode.setText("Erode: "+str(self.dic['Erode']))
                self.ui.label_Dilate.setText("Dilate: "+str(self.dic['Dilate']))                
                self.frame = cv.QueryFrame(self.capture)
                try: (self.track_window, self.frame,_,self.range_list)= multiples_objetos(self.hist,self.frame,self.dic,self.track_window,self.range_list)# frame viene ya dibujado
                except: pass

                if is_rect_nonzero(self.track_window):
                    self.cont=self.cont+1
                if self.cont>self.dic["cuenta"]:
                    self.cont=0
                    self.track_window=(0,0,0,0)                        
                if self.dic["rectangulo"]:
                    cv.Rectangle(self.frame, (self.dic["rectangulo"][0],self.dic["rectangulo"][1]), (self.dic["rectangulo"][2],self.dic["rectangulo"][3]),[255,0,0],2,8, 0)  # rectangulo de trabajo
                    cv.Rectangle(self.frame, (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]-int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]),
                                         (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]+int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]+int(320/self.dic["lineablanca"])),[255,0,0],1,8, 0)  # rectangulo de posicion del brazo
                
                self.image = self.build_image(self.frame)
                self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents,10)

        if not self.ui.pushButton_probar.isChecked():
            self._timer.stop()                                      # por las dudas vuelvo a para el timrer            
            self.ui.menubar.setEnabled(True)  # desactivo barra de menu
            self.ui.pushButton_conf.setEnabled(True)# desactivo conf
            self.ui.groupBox_conf.setEnabled(False)
            self.ui.tabWidget.setTabEnabled(0, True)  # anulo tab uno hasta q toggle boton conf            
            self.ui.groupBox_probar.setEnabled(False)# activo grupo probar, por las dudas    
            self.ui.pushButton_probar.setText("Probar")
            self._timer.start(10)
            
#-----------------------------------------------------------------------------


    def calibrar(self):
        """ Rutina para ajustes del area de trabajo """
        if self.ui.pushButton_conf.isChecked() and not self.ui.pushButton_probar.isChecked():
            self.ui.menubar.setEnabled(False)  # desactivo barra de menu
            self.ui.pushButton_probar.setEnabled(False)# desactivo probar
            self.ui.groupBox_probar.setEnabled(False)# desactivo grupo probar, por las dudas    
            self.ui.pushButton_conf.setText("Aceptar")
            self._timer.stop()
            self.ui.tabWidget.setTabEnabled(0, False)  # anulo tab uno hasta q toggle boton conf
            self.ui.groupBox_conf.setEnabled(True)
            self.selection=(0,0,0,0)
            self.posicion=None
            self.inicio_arrastre=None # cuando tiene algo es una tupla: (0,0)
 
            while self.ui.pushButton_conf.isChecked():
                self.frame = cv.QueryFrame(self.capture)
                if not self.ui.pushButton_dib_hist.isChecked():
                    self.ui.pushButton_conf.setEnabled(True)
                    self.ui.pushButton_dib_hist.setText("Dibujar Histograma")
                    self.ui.label_conf.setText("Dibuje el area de trabajo") #"ingrese area de trabajo"

#------si inicio arrastre la linea es mas fina, q cuando dibujo el cuaro azul-----------------------------

                    if self.inicio_arrastre:
                        cv.Rectangle(self.frame, (self.dic["rectangulo"][0],self.dic["rectangulo"][1]), (self.dic["rectangulo"][2],self.dic["rectangulo"][3]),[255,0,0],1,8, 0)
                        cv.Line(self.frame, (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]-10), (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]+10), [25,20,175], thickness=2, lineType=cv.CV_AA, shift=0)
                        cv.Rectangle(self.frame, (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]-int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]),
                                         (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]+int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]+int(320/self.dic["lineablanca"])),[255,0,0],1,8, 0)  # rectangulo de posicion del brazo                                    
                    elif is_rect_nonzero(self.dic["rectangulo"]): 
                        cv.Rectangle(self.frame, (self.dic["rectangulo"][0],self.dic["rectangulo"][1]), (self.dic["rectangulo"][2],self.dic["rectangulo"][3]),[255,0,0],2,8, 0)
                        cv.Rectangle(self.frame, (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]-int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]),
                                         (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]+int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]+int(320/self.dic["lineablanca"])),[255,0,0],2,8, 0)  # rectangulo de posicion del brazo                    
                
                        cv.Line(self.frame, (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]-10), (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]+10), [25,20,175], thickness=2, lineType=cv.CV_AA, shift=0)

                        cv.Line(self.frame, (300,240), (340,240), [255,255,255], thickness=2, lineType=cv.CV_AA, shift=0)	#linea de 40 px
                        cv.Line(self.frame, (300,230), (300,250), [255,100,50], thickness=2, lineType=8, shift=0) 
                        cv.Line(self.frame, (340,230), (340,250), [255,100,50], thickness=2, lineType=8, shift=0)

 #--------------------dibujo area para hist------------------------------------                       

                if self.ui.pushButton_dib_hist.isChecked():
                    self.ui.pushButton_conf.setEnabled(False) # me aseguro de no tocar el boton configurar
                    self.ui.label_conf.setText("Dibuje el area de histograma") 
                    self.ui.pushButton_dib_hist.setText("Confirmar")

    #--------------------si suelto mas desaparece el cuadrito----------------------------------   
                    
                    if self.inicio_arrastre:

#--------------------mientras arrastro calculo hist---------------------------------------------------------
                        if is_rect_nonzero(self.hist_map):
                            self.hist=self.calc_hist(self.frame,self.hist_map,self.hist)  
             
#--------------------siempre dibujo el cuadro azul---------------------------------------------------------
                    cv.Rectangle(self.frame, (self.dic["rectangulo"][0],self.dic["rectangulo"][1]), (self.dic["rectangulo"][2],self.dic["rectangulo"][3]),[255,0,0],1,8, 0)
                    cv.Rectangle(self.frame, (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]-int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]),
                                         (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]+int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]+int(320/self.dic["lineablanca"])),[255,0,0],1,8, 0)  # rectangulo de posicion del brazo                                    
                    cv.Line(self.frame, (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]-10), (self.dic["rectangulo"][0]+(self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2,self.dic["rectangulo"][1]+10), [25,20,175], thickness=2, lineType=cv.CV_AA, shift=0)

                self.histimg = IplQImage(self.hue_histogram_as_image(self.hist))
                self.ui.label_hist.setPixmap(QtGui.QPixmap.fromImage(self.histimg)) 
                self.image = self.build_image(self.frame)
                self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents,8)

        if not self.ui.pushButton_conf.isChecked():
            self.ui.pushButton_conf.setText("Configurar")
            self.ui.pushButton_dib_hist.setText("Dibujar Histograma")
            self._timer.stop()                                      # por las dudas vuelvo a para el timrer
            self.ui.tabWidget.setTabEnabled(0, True)  # activo tab uno 
            self.ui.menubar.setEnabled(True)  # activo barra de menu
            self.ui.groupBox_conf.setEnabled(False)     # desactivo box de configuracion
            self.ui.pushButton_probar.setEnabled(True)# activo probar
            self.ui.groupBox_probar.setEnabled(False)# desactivo grupo probar
            
    #--------------------renuevo el diccionario---------------------------------------------------------------
            self.dic["lineablanca"]=float(self.ui.doubleSpinBox_px2cm.value())
            # el rectangulo se actualiza en mouse event
            self.dic["crit"]=int(self.ui.comboBox_size.currentIndex())
            self.dic["t_min"]=float(self.ui.doubleSpinBox_cmMin.value())
            self.dic["t_max"]=float(self.ui.doubleSpinBox_cmMax.value())
            (v_min,v_max,x_min,x_max)=cv.GetMinMaxHistValue(self.hist)
                
            self.dic["hist"][0],self.dic["hist"][1],self.dic["hist"][2],self.dic["hist"][3],_,_,_,_=BW_hist(self.hist)  # aca hay q armar una ventana

            self.ui.consola.append(">>>Calibracion realizada con exito, listo para empezar\n")

#--------------------------------actualizo tab iniciar---------------------------------------
            self.ui.label_config.clear()
            self.ui.label_config.setText("Rectangulo: "+str(self.dic["rectangulo"])+"\n"+
                                          "Criterio: "+str(self.ui.comboBox_size.currentText())+"\n"+
                                            "Tamano: "+str(self.dic["t_min"])+" a "+str(self.dic["t_max"])+"cm2\n"+
                                            "Histograma: "+str(self.dic["hist"])+"\n"+
                                           "Linea blanca: "+str(self.dic["lineablanca"])+"\n"+
                                         "Interpolacion (N frames): "+str(self.dic["cuenta"]))
            self._timer.start(10)

#--------------------------------------------------------------------------------------------

    def iniciar(self):
        if self.ui.pushButton_iniciar.isChecked():
            self.ui.menubar.setEnabled(False)  # desactivo barra de menu
            if  not self.dic["is_disp"]:            # si no hay pinguino no puedo iniciar
                self.ui.pushButton_iniciar.setChecked(False)
                self.ui.consola.append(">>>No se puede inciar, el dispositivo no constesta\n")
                self.ui.menubar.setEnabled(True)
                return

            self._timer.stop()
            self.ui.pushButton_iniciar.setText("Parar")
            self.ui.tabWidget.setTabEnabled(1, False)  # anulo tab uno hasta q toggle boton parar
            self.cont=0
            #----------algoritmos de buqueda--------------------------------------------------------------
            while self.ui.pushButton_iniciar.isChecked():

                self.frame = cv.QueryFrame(self.capture)
                if not self.dic["buscar"]:
                    if self.cont==0:
                        inicio=time.time()     

                    try: 
                        (self.track_window, self.frame,self.tupla,self.range_list)= multiples_objetos(self.hist,self.frame,self.dic,self.track_window,self.range_list)# frame viene ya dibujado
                    except:
                        self.ui.consola.append(">>>No hay mas objetos\n")
                        self.cont=0
                        self.dic["destino"]=(0,0)
                        self.dic["centro"]=[]
                        self.track_window=(0,0,0,0)
                        inicio=time.time()

                    if is_rect_nonzero(self.track_window):
                        self.dic["centro"].append(self.tupla[0])
                        self.dic["centro"].append(self.tupla[1])
                        self.cont=self.cont+1

                    if self.cont>self.dic["cuenta"] and self.dic["rectangulo"]:
                        self.dic["t_frames"]=time.time()-inicio
                        self.dic["destino"]=(0,0)
                        self.dic["buscar"]=True
                        self.cont=0

                if self.dic["buscar"] and self.dic["destino"]!=(0,0):   # dibujo una sola vez el destino, si es que llega
                    cv.Circle(self.frame,self.dic["destino"],4,[0,255,0],-1)

                if self.dic["rectangulo"]:
                    cv.Rectangle(self.frame, (self.dic["rectangulo"][0],self.dic["rectangulo"][1]), (self.dic["rectangulo"][2],self.dic["rectangulo"][3]),[255,0,0],2,8, 0)  # rectangulo de trabajo
                    cv.Rectangle(self.frame, (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]-int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]),
                                         (((self.dic["rectangulo"][2]-self.dic["rectangulo"][0])/2+self.dic["rectangulo"][0]+int(360/self.dic["lineablanca"])),
                                          self.dic["rectangulo"][1]+int(320/self.dic["lineablanca"])),[255,0,0],1,8, 0)  # rectangulo de posicion del brazo
                
                self.image = self.build_image(self.frame)
                self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents,10)

            #---------fin algoritmo de busqueda-------------------------------------------------------
        if not self.ui.pushButton_iniciar.isChecked():
            self._timer.start(10)
            self.dic["centro"]=[0]
            self.cont=0
            self.ui.pushButton_iniciar.setText("Iniciar")
            self.dic['is_second']=True 
            self.ui.tabWidget.setTabEnabled(1, True)  # activo ta 2 de calibracion
            self.ui.menubar.setEnabled(True)  # activo barra de menu

#-----------------------------------------------------------------------------

    def conectar(self): 
            self.pinguino=pinguino(self.dic)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('conectado'), self.conectado)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('errorconexion'), self.errorconexion)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('buscando'), self.buscando)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('nocontesta'), self.nocontesta)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('objetofuera'), self.objetofuera)
            self.pinguino.start()

#-----------------------------------------------------------------------------

    def errorconexion(self):
        self.dic["is_disp"]=False
        self.pinguino.terminate()
        reply = QtGui.QMessageBox.critical(self, "Error",
                "No se ha detectado el dispositivo, revise la conexion",
                QtGui.QMessageBox.Abort , QtGui.QMessageBox.Retry)
        if reply == QtGui.QMessageBox.Abort:
            self.ui.consola.append(">>>No se ha detectado el dispositivo, revise la conexion\n")
        elif reply == QtGui.QMessageBox.Retry:
            self.conectar()
        

    def buscando(self):
        self.ui.consola.append(">>>Buscando objeto!!\n")

    def nocontesta(self):
        self.ui.consola.append(">>>El dispositivo no contesta\n")
        self.dic["is_disp"]=False

    def objetofuera(self):
        self.ui.consola.append(">>>Objeto fuera de area\n")

    def conectado(self):
        self.ui.consola.append(">>>Dispositivo conectado\n")
        self.dic["is_disp"]=True

#-----------------------------------------------------------------------------

    def cerrar(self):
        self._timer.stop()   
        reply = QtGui.QMessageBox.question(self, "Salir?",
                QtGui.QApplication.translate("Aplicacion 1", "Desea cerrar la aplicacion?", None, QtGui.QApplication.UnicodeUTF8),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()
        if reply == QtGui.QMessageBox.No:
            self._timer.start(10)   

#-----------------------------------------------------------------------------

    def acerca(self):
        self._timer.stop()
        self.ventana_acerca=acerca()
        QtCore.QObject.connect(self.ventana_acerca,QtCore.SIGNAL('cerrar_acerca'),self._timer.start)
        self.ventana_acerca.show()

#-----------------------------------------------------------------------------

    def contacto(self):
        self._timer.stop()
        self.ventana_contacto=contacto()
        QtCore.QObject.connect(self.ventana_contacto,QtCore.SIGNAL('cerrar_contacto'),self._timer.start)
        self.ventana_contacto.show()

#-----------------------------------------------------------------------------

    def instrucciones(self):
        self._timer.stop()
        self.ventanaInstrucciones=instrucciones()
        QtCore.QObject.connect(self.ventanaInstrucciones,QtCore.SIGNAL('cerrar_instrucciones'),self._timer.start)
        self.ventanaInstrucciones.show()

#-----------------------------------------------------------------------------

    def iraplicacion2(self):
        self.pinguino.close()
        self._timer.stop()
        del(self.capture)
        self.ventana=aplicacion2.Aplicacion()
        self.ventana.show()
        self.close()

#-----------------------calculo de histograma------------------------------------------------------

    def calc_hist(self,frame,hist_map,hist):
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
        cv.Split(hsv, hue, None, None, None)        
        sub = cv.GetSubRect(frame, hist_map)
        save = cv.CloneMat(sub)
        cv.ConvertScale(frame, frame, 0.5)
        cv.Copy(save, sub)
        x,y,w,h = hist_map
        cv.Rectangle(frame, (x,y), (x+w,y+h), (255,255,255))
        sel = cv.GetSubRect(hue, hist_map)
        cv.CalcArrHist( [sel], hist, 0)
        (_, max_val, _, x_max) = cv.GetMinMaxHistValue( hist)
        if max_val != 0:
            cv.ConvertScale(hist.bins, hist.bins, 255. / max_val)
        return hist

#-----------------------------------------------------------------------------

class IplQImage(QtGui.QImage):
    """ Clase para conversion de iplimages a qimages """
    def __init__(self,iplimage):
        alpha = cv.CreateMat(iplimage.height,iplimage.width, cv.CV_8UC1)
        cv.Rectangle(alpha, (0, 0), (iplimage.width,iplimage.height), cv.ScalarAll(255) ,-1)
        rgba = cv.CreateMat(iplimage.height, iplimage.width, cv.CV_8UC4)
        cv.Set(rgba, (1, 2, 3, 4))
        cv.MixChannels([iplimage, alpha],[rgba], [
        (0, 0), # rgba[0] -> bgr[2]
        (1, 1), # rgba[1] -> bgr[1]
        (2, 2), # rgba[2] -> bgr[0]
        (3, 3)  # rgba[3] -> alpha[0]
        ])
        self.__imagedata = rgba.tostring()
        super(IplQImage,self).__init__(self.__imagedata, iplimage.width, iplimage.height, QtGui.QImage.Format_RGB32)


 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Aplicacion()
    a.show()
    sys.exit(app.exec_())
