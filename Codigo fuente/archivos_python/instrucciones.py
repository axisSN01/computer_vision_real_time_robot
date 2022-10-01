# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instrucciones.ui'
#
# Created: Sat Mar  9 20:11:05 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_instrucciones(object):
    def setupUi(self, instrucciones):
        instrucciones.setObjectName(_fromUtf8("instrucciones"))
        instrucciones.resize(520, 495)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(instrucciones.sizePolicy().hasHeightForWidth())
        instrucciones.setSizePolicy(sizePolicy)
        instrucciones.setMinimumSize(QtCore.QSize(520, 495))
        instrucciones.setMaximumSize(QtCore.QSize(522, 496))
        self.horizontalLayout = QtGui.QHBoxLayout(instrucciones)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textBrowser = QtGui.QTextBrowser(instrucciones)
        self.textBrowser.setMinimumSize(QtCore.QSize(520, 490))
        self.textBrowser.setMaximumSize(QtCore.QSize(520, 490))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.horizontalLayout.addWidget(self.textBrowser)

        self.retranslateUi(instrucciones)
        QtCore.QMetaObject.connectSlotsByName(instrucciones)

    def retranslateUi(self, instrucciones):
        instrucciones.setWindowTitle(QtGui.QApplication.translate("instrucciones", "instrucciones", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("instrucciones", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.15094pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Se deben seguir las siguientes instrucciones y recomendaciones para lograr el funcionamiento óptimo de sistema.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">..:: Aplicación 1 ::..</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">1)</span><span style=\" font-size:11pt;\"> Iniciar la calibración ingresando en la pestaña &quot;Calibración&quot; y haciendo clic en el botón &quot;Configurar&quot;.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">2)</span><span style=\" font-size:11pt;\"> Realice la medición de la línea blanca que se muestra en pantalla. Para ello coloque una regla en el espacio de trabajo y mida, a través de la pantalla, el tamaño de la línea. Ingrese dicho valor en el casillero correspondiente.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">3)</span><span style=\" font-size:11pt;\"> Seleccione el criterio a utilizar y configure los tamaños mínimo y máximo (en cm2) de los objetos a detectar.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">4)</span><span style=\" font-size:11pt;\"> Haciendo clic en la pantalla (donde se muestran las imágenes capturadas) y arrastrando el mouse, puede seleccionarse el espacio de trabajo. El brazo robot debe posicionarse exactamente en el recuadro color azul en la parte superior del espacio de trabajo.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">5) </span><span style=\" font-size:11pt;\">Para seleccionar el color del objeto a detectar debe presionar en el botón &quot;Dibujar Histograma&quot;. Una vez activo, seleccione en pantalla (donde se muestran las imágenes capturadas) el color deseado. Es preferible que el objeto a detectar se encuentre en el espacio de trabajo para poder obtener el color exacto.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">6)</span><span style=\" font-size:11pt;\"> Una vez configurado el sistema, debe hacer clic en el botón &quot;Aceptar&quot; para aplicar los cambios.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">7)</span><span style=\" font-size:11pt;\"> Para asegurarse el buen funcionamiento de la aplicación utilizando la configuración antes realizada, debe presionar en el botón &quot;Probar&quot;.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">8)</span><span style=\" font-size:11pt;\"> Para realizar el ajuste fino de la calibración, se recomienda poner a 0 el valor de &quot;Dilate&quot; e ir aumentando &quot;Erode&quot; hasta lograr que se detecte correctamente el objeto de interés (se dibujan puntos de color rojo por cada detección realizada). Una vez hecho esto, aumentar el &quot;Dilate&quot; hasta que se dibuje correctamente un circulo rojo alrededor del objeto.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">9) </span><span style=\" font-size:11pt;\">Se debe configurar también la cantidad de posiciones que deberá obtener el sistema hasta realizar la interpolación (cálculo de posición futura). Un valor elevado generará un mayor retardo pero logrando mayor presición en la interpolación. Un valor bajo premitirá que la detección se realice mas rápidamente pero a costa de una mala presición.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">10)</span><span style=\" font-size:11pt;\"> Si se logra una correcta detección, haga clic en el boton &quot;Aceptar&quot; y pase a la pestaña &quot;Iniciar&quot; para poder dar inicio a la aplicación. En caso contrario, se recomienda realizar la calibración de nuevo, en especial, el paso 5.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">11)</span><span style=\" font-size:11pt;\"> Es recomendable que se guarde el archivo de configuración ingresando a &quot;Opciones&quot;--&gt;&quot;Guardar Configuración&quot;. Si se desea abrir un archivo de configuración guardado previamente, ingrese a &quot;Opciones&quot;--&gt;&quot;Cargar Configuración&quot; e inmediatamente se aplicará al sistema.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">..:: Aplicación 2 ::..</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:600;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Debe tener en cuenta que esta aplicación requiere de un fondo uniforme del espacio de trabajo y una iluminación omnidireccional y difusa para que funcione correctamente.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">1)</span><span style=\" font-size:11pt;\"> Iniciar la calibración ingresando en la pestaña &quot;Calibración&quot;. Asegurese que su mano no aparezca en pantalla y que solo se esté capturando el fondo del espacio de trabajo. Haga clic en el botón &quot;Calibrar&quot;.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">2) </span><span style=\" font-size:11pt;\">Coloque los valores de &quot;Erode&quot; y &quot;Dilate&quot; en 0. A continuación coloque su mano en el espacio de trabajo y modifique el valor de &quot;Threshold min&quot; hasta que su mano se muestre en color blanco. </span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">3)</span><span style=\" font-size:11pt;\"> Modifique &quot;Erode&quot; para quitar el ruido de la pantalla y evitar que se detecten pixeles erroneos.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">4)</span><span style=\" font-size:11pt;\"> Modifique &quot;Dilate&quot; para lograr que su mano se muestre dibujada perfectamente en color blanco y sin cortes.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">5) </span><span style=\" font-size:11pt;\">Presione en el botón &quot;Ver detección&quot; para asegurarse que la detección de su mano se realice correctamente. Se debe dibujar un contorno color verde alrededor de la misma.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">6)</span><span style=\" font-size:11pt;\"> Realice la medición de la línea que se muestra en pantalla. Para ello coloque una regla en el espacio de trabajo y mida, a través de la pantalla, el tamaño de la línea. Ingrese dicho valor en el casillero correspondiente.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">7)</span><span style=\" font-size:11pt;\"> Si se logra una correcta detección, haga clic en el boton &quot;Aceptar&quot; (manteniedo la mano en el espacio de trabajo) y pase a la pestaña &quot;Iniciar&quot; para poder dar inicio a la aplicación. En caso contrario, se recomienda realizar la calibración de nuevo, en especial, el paso 5.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">8)</span><span style=\" font-size:11pt;\"> Es recomendable que se guarde el archivo de configuración ingresando a &quot;Opciones&quot;--&gt;&quot;Guardar Configuración&quot;. Si se desea abrir un archivo de configuración guardado previamente, ingrese a &quot;Opciones&quot;--&gt;&quot;Cargar Configuración&quot; e inmediatamente se aplicará al sistema.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

