#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import serial

################### Comunicacion #############################
#  Maneja la parte de comunicacion con el microcontrolador   # 
##############################################################
class Comunicacion:
	ser = None
	WXK_UP = 315
	WXK_DOWN = 317
	WXK_LEFT = 314
	WXK_RIGHT = 316
	comando = {WXK_UP: 'q', WXK_DOWN: 'w', WXK_LEFT: 'e', WXK_RIGHT: 'r'};
	detener = 't'

	hayComandoEnviado = None

	def __init__(self, puerto, baud):
		self.ser = serial.Serial(puerto, baud)
		self.hayComandoEnviado = False
	
	def enviar(self, char):
		self.ser.write(char)

	def manejar_tecla(self, tecla, se_presiono):
		if(se_presiono and not self.hayComandoEnviado):
			self.enviar(self.comando[tecla])
			self.hayComandoEnviado = True
		else:
			self.hayComandoEnviado = False
			self.enviar(self.detener)


#################### Ventana ########################
#         Maneja la parte grafica del programa      # 
#####################################################
class Ventana(wx.Frame):
    com = None

    def __init__(self, title, com):
    	self.com = com

        wx.Frame.__init__(self, None, title=title, size=(350,200))
        self.iniciarUI()
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

    def iniciarUI(self):   
        panel = wx.Panel(self)
        self.SetSize((250, 200))
        self.Centre()
        self.Show(True)          

    def onKeyDown(self, event):
    	#print event.GetKeyCode()
        self.com.manejar_tecla(event.GetKeyCode(), True)  

    def onKeyUp(self, event):
    	self.com.manejar_tecla(event.GetKeyCode(), False)


def main():
    puerto = "/dev/ttyACM0"
    baud = 9600
    com = Comunicacion(puerto, baud)
    ex = wx.App()
    Ventana("Prueba control remoto",com)
    ex.MainLoop()    


if __name__ == '__main__':
    main()   