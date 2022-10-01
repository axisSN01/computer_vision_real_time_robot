from PyQt4 import QtCore, QtGui
from acerca import Ui_acerca
from contacto import Ui_contacto
from instrucciones import Ui_instrucciones
import sys

class acerca(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ventana=Ui_acerca()
        self.ventana.setupUi(self)
        self.ventana.pushButton.clicked.connect(self.anterior)
        self.ventana.pushButton_2.clicked.connect(self.siguiente)
        self.foto=0
        self.center()

    def anterior(self):
        if self.foto>0: self.foto=self.foto-1
        self.ventana.label.setPixmap(QtGui.QPixmap(sys.path[0]+'/images/'+str(self.foto)+'.jpg'))        

    def siguiente(self):
        self.ventana.label.setPixmap(QtGui.QPixmap(sys.path[0]+'/images/'+str(self.foto+1)+'.jpg'))     
        self.foto=self.foto+1

    def closeEvent(self, event):
        self.emit(QtCore.SIGNAL('cerrar_acerca'))
        event.accept()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

#----------------------------------------------------------------------

class instrucciones(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ventana=Ui_instrucciones()
        self.ventana.setupUi(self)
        self.center()

    def closeEvent(self, event):
        self.emit(QtCore.SIGNAL('cerrar_instrucciones'))
        event.accept()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

#----------------------------------------------------------------------

class contacto(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ventana=Ui_contacto()
        self.ventana.setupUi(self)
        self.center()

    def closeEvent(self, event):
        self.emit(QtCore.SIGNAL('cerrar_contacto'))
        event.accept()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


