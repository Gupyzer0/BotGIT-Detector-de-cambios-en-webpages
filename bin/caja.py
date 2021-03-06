import sys, threading, requests, hashlib, pprint, pyperclip, webbrowser, functools
sys.path.append("../interfaz")
sys.path.append("../bd")

from PyQt4 import QtCore,QtGui
from qt4BaseDatos import baseDatos
#Modulos visuales
#Modulos visuales
from cajaInterfaz import Widget_Caja

try:
	_fromUtf8 = QtCore.QString._fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

class Caja(QtGui.QWidget):
	def __init__(self, portal, ente, lista, ministerio, parent):
		super(Caja, self).__init__(parent)
		self.ui = Widget_Caja(parent)#Interfaz grafica de la caja
		self.ente = ente
		self.ministerio = ministerio
		self.portal = portal
		self.lista = lista #{'url': ,'direccionArchivo': ,'md5': ,'diff': ,'ultPorcCambio':, 'porcDetectCambio':,'estatus': }
		self.porcDetectarDiferencia = 0 #porcentaje de diferencia en la cual se detecta una diferencia valida, 20 por defecto
		self.estatus = "ok"
		self.porcPromedioCambio = 0 #porcentaje promedio de las detecciones de todas las URL
		self.ui.texto_porcentaje.setText(str(self.porcDetectarDiferencia))
		self.ui.texto_porcentaje_cambio_promedio.setText(str(baseDatos.seleccionar_deteccion_cambio_actual(self.portal)))
		self.ui.groupBox.setTitle(_fromUtf8(portal))
		self.ui.dial_porcentaje.valueChanged.connect(self.setPorcDetectarDiferencia)

	def setPorcDetectarDiferencia(self, valor):
		self.porcDetectarDiferencia = valor #aunque ... poco importa cambiarlo
		self.ui.texto_porcentaje.setText(str(valor))
		baseDatos.set_porcentaje_diferencia_portal(valor,self.portal)
				
		#Diferente a la anterior usada para manejar los valores del dial (0-999), este los maneja desde la base datos
		#por lo que no es necesario dividirlo entre 10
	def setPorcDetectarDiferenciaBd(self, valor):
		self.porcDetectarDiferencia = valor
		self.ui.texto_porcentaje.setText(str(valor))
		baseDatos.set_porcentaje_diferencia_portal(valor, self.portal)
		
	def setGetPorcPromedioCambio(self):
		self.porcPromedioCambio = round(sum(elem['ultPorcCambio'] for elem in self.lista) / len(self.lista),3)
		porcentaje = round(self.porcPromedioCambio,3)
		baseDatos.set_porc_deteccion_cambio_actual(porcentaje,self.portal)
		self.ui.texto_porcentaje_cambio_promedio.setText(str(porcentaje))
		return porcentaje

	def porc_promedio_actual_set(self):
		self.setPorcDetectarDiferenciaBd(self.setGetPorcPromedioCambio())
		
	#reactiva el boton de comparar YA luego de terminada la comparacion
	def manejarLista(self, lista):
		self.ui.btn_compararYa.setDisabled(0)
