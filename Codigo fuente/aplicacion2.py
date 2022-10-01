#!/usr/bin/python -d
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from archivos_python import *
from archivos_python.ventana_principal2 import Ui_ventana
from archivos_python.pinguino2 import *
import cv, math
from ConfigParser import RawConfigParser
import time
import aplicacion1

# diccionario global de variables y para debug
dic={"centro_masa":(0.0,0.0),"is_disp":False,"z":0.0,"ir":False,"is_hand":False,"is_open":True,"ThresMin":0,"Erode":0,"Dilate":0,"linea":0}

class Aplicacion(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ventana()
        self.ui.setupUi(self)
        try:
            self.capture = cv.CreateCameraCapture(-1)
            cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_BRIGHTNESS,0.5)
            self.backGround=cv.CloneImage(cv.QueryFrame(self.capture))  
        except:
            self.ui.consola.append(">>>Imposible leer camara (reinicie)\n") 
        self.frame=None
        self._frame = None
        global dic
        self.dic=dic
        self.ui.groupBox_conf.setEnabled(False)
        self.ui.botoncalib.clicked.connect(self.calibrar)
        self.ui.pushButton_iniciar.clicked.connect(self.iniciar)
        self.ui.actionCerrar.triggered.connect(self.cerrar)
        self.ui.actionAcerca.triggered.connect(self.acerca)
        self.ui.actionInstrucciones.triggered.connect(self.instrucciones)
        self.ui.actionContacto.triggered.connect(self.contacto)
        self.ui.actionCargar.triggered.connect(self.cargar_configuracion)
        self.ui.actionGuardar.triggered.connect(self.guardar_configuracion)
        self.ui.actionAp1.triggered.connect(self.iraplicacion1)
        self.cargar_configuracion()                             #cargo configuracion inicial
        self.conectar()                        #inicializo comunicacion con arduino
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.mostrar)
        self._timer.start(5)
        self.center()

#-----------------------------------------------------------------------------

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

#-----------------------------------------------------------------------------

    def cargar_configuracion(self):
        try:
            # leo .conf
            self.ui.consola.append(">>>Cargando configuracion\n")
            self.config=RawConfigParser()
            archivo=open(sys.path[0]+'/config/calib_app2.conf','r')
            self.config.readfp(archivo)
            self.dic['ThresMin']=int(self.config.get("Valores","ThresMin"))
            self.dic['Erode']=int(self.config.get("Valores","Erode"))
            self.dic['Dilate']=int(self.config.get("Valores","Dilate"))
            self.dic['linea']=float(self.config.get("Linea","Tamaño"))
            archivo.close()

            # set tab config

            self.ui.label_config.clear()
            self.ui.label_config.setText(  "ThresMin: "+str(self.dic["ThresMin"])+"\n"+
                                           "Erode: "+str(self.dic["Erode"])+"\n"+
                                           "Dilate: "+str(self.dic["Dilate"])+"\n"+
                                            "Linea: "+str(self.dic["linea"])+" cm")

            # cargar imagen patron

            self.img_patronRGB=cv.LoadImage(sys.path[0]+'/config/patron_app2.tif',3)
            self.img_patron=cv.LoadImage(sys.path[0]+'/config/patron_app2.tif',0)

            self.ui.consola.append(">>>Configuracion cargada con exito!!\r\n")  

        except:
            self.ui.consola.append(">>>No se pudo cargar la configuracion, por favor, realice la calibracion\r\n")

        self.ui.ThresMin.setValue(self.dic['ThresMin'])
        self.ui.Erode.setValue(self.dic['Erode'])
        self.ui.Dilate.setValue(self.dic['Dilate'])
        self.ui.linea.setValue(self.dic['linea'])
   
#----------------------------------------------------------------------

    def guardar_configuracion(self):
        self.config=RawConfigParser()
        archivo=open(sys.path[0]+'/config/calib_app2.conf','r')
        self.config.readfp(archivo)
        self.config.set("Valores","ThresMin",self.dic['ThresMin'])
        self.config.set("Valores","Erode",self.dic['Erode'])
        self.config.set("Valores","Dilate",self.dic['Dilate'])
        self.config.set("Linea","Tamaño",self.ui.linea.value())
        archivo=open(sys.path[0]+'/config/calib_app2.conf',"w")
        self.config.write(archivo)
        self.ui.consola.append(">>>Configuracion guardada!! "+time.strftime("%a, %d/%b/%y, %H:%M:%S",time.gmtime())+"\n")       
        archivo.close()
        cv.SaveImage(sys.path[0]+'/config/patron_app2.tif',self.color_mask2) #grabo mano patron
        
#----------------------------------------------------------------------

    def build_image(self, frame):
        """ Transforma iplimages a qimages """
        if not self._frame:
            self._frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels)
        if frame.origin == cv.IPL_ORIGIN_TL:
            cv.Copy(frame, self._frame)
        else:
            cv.Flip(frame, self._frame, 0)
        return IplQImage(self._frame)

    def mostrar(self):
            self.frame = cv.QueryFrame(self.capture)
            self.image = self.build_image(self.frame)
            self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))

#-----------------------------------------------------------------------------

    def calibrar(self):
        """ Rutina para ajustes del area de trabajo """
        if self.ui.botoncalib.isChecked():
            self.backGround=cv.CloneImage(cv.QueryFrame(self.capture))  
            self.ui.menubar.setEnabled(False)  # desactivo barra de menu
            self.ui.botoncalib.setText("Aceptar")
            self._timer.stop()
            self.ui.tabWidget.setTabEnabled(0, False)  # anulo tab uno hasta q toggle boton conf
            self.ui.groupBox_conf.setEnabled(True)
            self.ScaleImage=cv.CreateImage((640,480),8,3)
            while self.ui.botoncalib.isChecked():
                self.dic['ThresMin']=self.ui.ThresMin.value() #renuevo el diccionario
                self.dic['Erode']=self.ui.Erode.value()
                self.dic['Dilate']=self.ui.Dilate.value()
                self.frame = cv.QueryFrame(self.capture)
                frame2=cv.CloneImage(self.frame)
                color_mask1 = cv.CreateImage(cv.GetSize(self.frame), 8, 1)  # 8
                self.color_mask2=cv.CloneImage(color_mask1)
                color_mask1= self.extractForeGround(self.frame,self.backGround,self.dic["ThresMin"],self.dic["Erode"],self.dic["Dilate"])
                try:               
                    frame2,self.color_mask2,_,_,_=self.CleanForeArm(color_mask1,self.frame)# aca tomo mi fanstama patron

#--------------------------me fijo que muestro, si BW o a color------------------------------
                    if self.ui.botonvista.isChecked():  #muestra la vista deteccion
                        cv.Line(frame2,(240,10),(340,10),[0,0,255],3) 
                        self.image = self.build_image(frame2)   

                    else: #muestra la vista binaria
                        color_mask2_rgb=cv.CreateImage((640,480),8,3)
                        cv.CvtColor(self.color_mask2,color_mask2_rgb,cv.CV_GRAY2BGR) 
                        self.image = self.build_image(color_mask2_rgb)
#------------------------------------------------------------------------------------------
                except: pass

                self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents,10)
                
        if not self.ui.botoncalib.isChecked():
            self.ui.botoncalib.setText("Configurar")
            self._timer.stop()                                      # por las dudas vuelvo a para el timrer
            self.ui.tabWidget.setTabEnabled(0, True)  # activo tab uno 
            self.ui.menubar.setEnabled(True)  # activo barra de menu
            self.ui.groupBox_conf.setEnabled(False)     # desactivo box de configuracion
            
            self.ui.consola.append(">>>Calibracion realizada con exito, listo para empezar\n")

            # actualizo tab iniciar

            self.ui.label_config.clear()
            self.ui.label_config.setText("ThresMin: "+str(self.dic["ThresMin"])+"\n"+
                                           "Erode: "+str(self.dic["Erode"])+"\n"+
                                           "Dilate: "+str(self.dic["Dilate"])+"\n"+
                                            "Linea: "+str(self.dic["linea"])+" cm")
            # mano patron
             
            cv.CvtColor(self.color_mask2, self.img_patronRGB, cv.CV_GRAY2BGR) # para guardar en rgb
            self.img_patron=cv.CloneImage(self.color_mask2)  # para guardar en gray scale
           
            self._timer.start(10)

#--------------------------------------------------------------------------------------------

    def iniciar(self):
        if self.ui.pushButton_iniciar.isChecked():
            self.ui.menubar.setEnabled(False)  # desactivo barra de menu
            self.font = cv.InitFont(5,1.0,1.0,1.0,1,8) # inicializo una fuente por si hay q escribir algo en pantalla
            self.hsv = cv.CreateImage((640,480), 8, 3)
            self.AreaInicial=0
            self.storage = cv.CreateMemStorage(0) # el bloque es de 64k, se instancia todo lo q es recurrente
            self.contourPatron= cv.FindContours(self.img_patron, self.storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            if  not self.dic["is_disp"]:            # si no hay pinguino no puedo iniciar
                self.ui.pushButton_iniciar.setChecked(False)
                self.ui.menubar.setEnabled(True)  # desactivo barra de menu
                self.ui.consola.append(">>>No se puede inciar, el dispositivo no constesta\n")
                return

            self._timer.stop()
            self.ui.pushButton_iniciar.setText("Parar")
            self.ui.tabWidget.setTabEnabled(1, False)  # anulo tab uno hasta q toggle boton parar
            contour=None
            self.ui.consola.append(">>>Para iniciar, encuadre su mano con el fantasma\n")

            while self.ui.pushButton_iniciar.isChecked():
                self.frame= cv.QueryFrame(self.capture)
                if not self.dic["is_hand"]:
                    frame2=cv.CloneImage(self.frame)
                    cv.AddWeighted(self.frame, 1, self.img_patronRGB, 0.3,0, self.frame) # pego fantasma
                    color_mask1 = cv.CreateImage(cv.GetSize(self.frame), 8, 1)
                    color_mask1= self.extractForeGround(frame2,self.backGround,self.dic["ThresMin"],self.dic["Erode"],self.dic["Dilate"])
                                        
                    try:
                        frame2,color_mask1,contour,_,_=self.CleanForeArm(color_mask1,frame2)# aca tomo mi fanstama patron
                        shape=cv.MatchShapes(contour,self.contourPatron,cv.CV_CONTOURS_MATCH_I2) # para mi la mejor es MATCH_I2
                        if shape<0.50:    #  Relacion de contornos, busqueda de formas
                            self.dic["is_hand"]=True
                            self.AreaInicial=cv.ContourArea(self.contourPatron)
                            area_auxiliar=self.AreaInicial
                    except: 
                        self.ui.consola.append(">>>No hay contorno, encuadre su mano con el fantasma\n")
                        self.dic['ir']=False
                        self.dic["is_hand"]=False
                if self.dic["is_hand"]:
                    frame2=cv.CloneImage(self.frame)
                    color_mask1 = cv.CreateImage(cv.GetSize(self.frame), 8, 1)
                    color_mask1= self.extractForeGround(self.frame,self.backGround,self.dic["ThresMin"],self.dic["Erode"],self.dic["Dilate"])
                    try: frame2,color_mask1,contour,hull,defects=self.CleanForeArm(color_mask1,self.frame)
                    except:
                        self.ui.consola.append(">>>No hay contorno, encuadre su mano con el fantasma\n")
                        self.dic['ir']=False
                        self.dic["is_hand"]=False
 
                    try:
                     # Calculo del centro de masa
                        M = cv.Moments(contour)
                        centroid_x = int(M.m10/M.m00)
                        centroid_y = int(M.m01/M.m00)          # centro de masa de la imagen
                        self.dic["centro_masa"]=(centroid_x,centroid_y)
                        cv.Circle(self.frame,(centroid_x,centroid_y),5,[0,0,255],-1)

                     # Calculo si es mano abierta o cerrada

                        hull2 = cv.ConvexHull2(contour,self.storage,return_points=1) # devuelve los x,y
                        contourArea=cv.ContourArea(contour)
                        hullArea=cv.ContourArea(hull2)
                        if contourArea/hullArea<=0.80:
                            cv.PutText(self.frame,"ABIERTO",(20,20),self.font,[0,0,250])
                            self.dic["is_open"]=True        #relacion de solidez de la mano
                        else: 
                            self.dic["is_open"]=False     # mano cerrada
                            cv.PutText(self.frame,"CERRADO",(20,20),self.font,[0,0,250])

                        # Distancia en z
                        if self.dic["is_open"]:
                            z=self.dic["linea"]*float(math.sqrt(contourArea))/100.0-self.dic["linea"]*float(math.sqrt(self.AreaInicial))/100.0
                            self.dic["z"]=29.0*z/(self.dic["linea"]*float(math.sqrt(60000))/100.0)
                        else:
                            z=self.dic["linea"]*float(math.sqrt(contourArea))/100.0+4.5-self.dic["linea"]*float(math.sqrt(self.AreaInicial))/100.0
                            self.dic["z"]=29.0*z/(self.dic["linea"]*float(math.sqrt(60000))/100.0)
                        if self.dic["z"]>0: 
                            self.dic['ir']=True
                        else: 
                            self.dic['ir']=False
                    except: 
                        self.ui.consola.append(">>>No hay contorno, encuadre su mano con el fantasma\n")
                        self.dic['ir']=False
                        self.dic["is_hand"]=False
                self.image = self.build_image(self.frame)
                self.ui.labelcamara.setPixmap(QtGui.QPixmap.fromImage(self.image))
                QtGui.QApplication.processEvents(QtCore.QEventLoop.AllEvents,10)

        if not self.ui.pushButton_iniciar.isChecked():
            self.dic["is_hand"]=False
            self.dic['ir']=False
            self._timer.start(5)
            self.ui.pushButton_iniciar.setText("Iniciar")
            self.ui.menubar.setEnabled(True)  # activo barra de menu
            self.ui.tabWidget.setTabEnabled(1, True)  # activo tab 2 de calibracion

#-----------------------------------------------------------------------------

    def conectar(self): 
            self.pinguino=pinguino(self.dic)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('conectado'), self.conectado)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('errorconexion'), self.errorconexion)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('nocontesta'), self.nocontesta)
            QtCore.QObject.connect(self.pinguino, QtCore.SIGNAL('nollega'), self.nollega)
            self.pinguino.start()

#-----------------------------------------------------------------------------

    def errorconexion(self):
        
        self.pinguino.terminate()
        reply = QtGui.QMessageBox.critical(self, "Error",
                "No se ha detectado el dispositivo, revise la conexion",
                QtGui.QMessageBox.Abort , QtGui.QMessageBox.Retry)
        if reply == QtGui.QMessageBox.Abort:
            self.ui.consola.append(">>>No se ha detectado el dispositivo, revise la conexion\n")
            self.dic["is_disp"]=False
        elif reply == QtGui.QMessageBox.Retry:
            self.conectar()      

    def nocontesta(self):
        self.ui.consola.append(">>>El dispositivo no contesta\n")
        self.dic["is_disp"]=False
    
    def nollega(self):
	    self.ui.consola.append(">>>El brazo no llega a la posicion deseada\n")

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
            self._timer.start(5)   

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
        self.ventana_instrucciones=instrucciones()
        QtCore.QObject.connect(self.ventana_instrucciones,QtCore.SIGNAL('cerrar_instrucciones'),self._timer.start)
        self.ventana_instrucciones.show()

#-----------------------------------------------------------------------------

    def iraplicacion1(self):
        self.pinguino.close()
        self._timer.stop()
        del(self.capture)
        self.ventana=aplicacion1.Aplicacion()
        self.ventana.show()
        self.close()

#-----------------------------------------------------------------------------

    def extractForeGround(self,image,background,thresholdMin,Erode,Dilate):
        """extrae mano de imagen, en BW"""
        differenceImage  =cv.CreateImage( cv.GetSize(image), 8, 3 )
        gray = cv.CreateImage( cv.GetSize(differenceImage), 8, 1 )
        frame2=cv.CreateImage(cv.GetSize(background),8,3)#$
        fondoG=cv.CreateImage(cv.GetSize(background),8,1)#$
        frameG=cv.CreateImage(cv.GetSize(background),8,1)#$
        cv.Split(background,None,fondoG,None,None)#$
        cv.CvtColor(image, frame2, cv.CV_RGB2HSV)#$
        cv.Split(frame2,None,frameG,None,None)#$
        cv.AbsDiff(frameG,fondoG,gray)#$
        cv.Not(gray,gray)#$
        cv.Threshold( gray,gray, thresholdMin, 255, cv.CV_THRESH_BINARY )  
        cv.Erode(gray,gray,None,Erode)       
        cv.Dilate(gray,gray,None,Dilate)       
        
        return gray        
#-----------------------------------------------------------------------------

#--------------------------funcion elimino ante brazo--------------------------
    def CleanForeArm(self,color_mask,frame2):
        """funcion que elimina antebrazo, devuelve rgb dibujado,gray,contour,hull,defects"""
        color_mask2=cv.CloneImage(color_mask)
        storage = cv.CreateMemStorage()
        try:
            contour = cv.FindContours(color_mask, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            hull = cv.ConvexHull2(contour,storage)  # devuelve los indices
            defects = cv.ConvexityDefects(contour,hull,storage)
            i=0
            punto_mayor=0
            while i <len(defects) and defects[i][2][1]<460:
                if defects[i][2][1]>punto_mayor:     # ahi tapo con un ractangulo
                    punto_mayor=defects[i][2][1]
                i=i+1
            if punto_mayor>50:
                cv.Rectangle(color_mask2,(0,punto_mayor), (640,480),(0,0,0),cv.CV_FILLED, lineType=8, shift=0)  # rectangulo que enmascara antebrazo

        #--------------------------dibujo rectangulo negro----------------------------------
            color_mask=cv.CloneImage(color_mask2) # reutilizo color_mask
            contour = cv.FindContours(color_mask, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            hull = cv.ConvexHull2(contour,storage)  # devuelve los indices
            defects = cv.ConvexityDefects(contour,hull,storage)
            i=0
            while i <len(defects):
                start,end,far,dist = defects[i]
                cv.Line(frame2,start,end,[0,255,0],2)
                cv.Circle(frame2,far,5,[0,0,255],-1)
                i=i+1
            return frame2, color_mask2, contour, hull, defects
        except:
            contour = None
            return frame2, color_mask2
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

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    a = Aplicacion()
    a.show()
    sys.exit(app.exec_())
