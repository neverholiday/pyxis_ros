#!/usr/bin/env python


import os
import sys

import cv2
import numpy as np

from PyQt4 import QtGui, QtCore

from image_widget import ImageWidget

class MainWindow( QtGui.QMainWindow ):

	def __init__( self, configPathStr ):

		super( MainWindow, self ).__init__()

		menuBar = self.menuBar()
		self.fileMenu = menuBar.addMenu( "File" )

		self.loadAction = QtGui.QAction( "Load", self )
		self.loadAction.setShortcut( "Ctrl+O" )
		self.fileMenu.addAction( self.loadAction )
		self.loadAction.triggered.connect( self.loadActionCallback )

		self.saveAction = QtGui.QAction( "Save", self )
		self.saveAction.setShortcut( "Ctrl+S" )
		self.fileMenu.addAction( self.saveAction )
		self.saveAction.triggered.connect( self.saveActionCallback )

		self.imageWidget = ImageWidget( configPathStr )
		self.setCentralWidget( self.imageWidget )

		self.setWindowTitle( "Color Calibrator V2.0" )

	def loadActionCallback( self ):

		loadPathStr = str( QtGui.QFileDialog.getOpenFileName( self, 'Open file', '~', '(*.ini)' ) )
		if len(loadPathStr) != 0:
			self.imageWidget.loadConfig( loadPathStr )
			print "Load : {}".format( loadPathStr )
			self.imageWidget.updateUI()


	def saveActionCallback( self ):

		savePathStr = str( QtGui.QFileDialog.getSaveFileName( self, 'Save file', 'config.ini', '(*.ini)' ) )
		if len(savePathStr) != 0:
			self.imageWidget.saveConfig( savePathStr ) 
			print "Save : {}".format( savePathStr )

if __name__ == "__main__":
	
	app = QtGui.QApplication( sys.argv )

	testConfigPath = "/home/neverholiday/work/ros_ws/src/pyxis/src/config_generator/config.ini"
	
	mainWindow = MainWindow(testConfigPath)
	mainWindow.show()

	sys.exit( app.exec_() )