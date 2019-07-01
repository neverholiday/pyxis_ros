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
		self.viewMenu = menuBar.addMenu( "View" )

		self.loadAction = QtGui.QAction( "Load", self )
		self.loadAction.setShortcut( "Ctrl+O" )
		self.fileMenu.addAction( self.loadAction )
		self.loadAction.triggered.connect( self.loadActionCallback )

		self.saveAction = QtGui.QAction( "Save", self )
		self.saveAction.setShortcut( "Ctrl+S" )
		self.fileMenu.addAction( self.saveAction )
		self.saveAction.triggered.connect( self.saveActionCallback )

		self.exportVideoAction = QtGui.QAction( "Export", self )
		self.exportVideoAction.setShortcut( "R" )
		self.fileMenu.addAction( self.exportVideoAction )
		self.exportVideoAction.triggered.connect( self.exportVideoCallback )

		self.toggleAction = QtGui.QAction( "Toggle", self )
		self.toggleAction.setShortcut( "T" )
		self.viewMenu.addAction( self.toggleAction )
		self.toggleAction.triggered.connect( self.toggleCallback )

		self.imageWidget = ImageWidget( configPathStr )
		self.setCentralWidget( self.imageWidget )

		self.previousPath = os.getenv( "HOME" )

		self.setWindowTitle( "Color Calibrator V2.0" )

		self.__toggleFlag = False
		self.__isRecord = False

	def loadActionCallback( self ):

		loadPathStr = str( QtGui.QFileDialog.getOpenFileName( self, 'Open file', '~', '(*.ini)' ) )
		if len(loadPathStr) != 0:
			self.previousPath = loadPathStr
			self.imageWidget.loadConfig( loadPathStr )
			print "Load : {}".format( loadPathStr )
			self.imageWidget.updateUI()


	def saveActionCallback( self ):

		savePathStr = str( QtGui.QFileDialog.getSaveFileName( self, 'Save file', self.previousPath, '(*.ini)' ) )
		if len(savePathStr) != 0:
			self.imageWidget.saveConfig( savePathStr ) 
			print "Save : {}".format( savePathStr )

	def toggleCallback( self ):
		
		print "{}".format( "Mask mode" if self.__toggleFlag else "Image mode" )

		self.imageWidget.imageLabel.setFlagMask( self.__toggleFlag )
		self.__toggleFlag = False if self.__toggleFlag else True

	def exportVideoCallback( self ):
		print "Record"
		if not self.__isRecord:
			savePathStr = str( QtGui.QFileDialog.getSaveFileName( self, 'Save file', self.previousPath, '(*.avi)' ) )
			self.imageWidget.imageLabel.constructRecorder( savePathStr )
			self.__isRecord = True
			self.imageWidget.imageLabel.setFlagRecord( self.__isRecord )
		else:
			self.imageWidget.imageLabel.setFlagRecord( self.__isRecord )
			
if __name__ == "__main__":
	
	app = QtGui.QApplication( sys.argv )

	testConfigPath = "/home/neverholiday/work/ros_ws/src/pyxis/src/config_generator/config.ini"

	# print __path__
	print os.path.abspath( os.path.curdir )
	
	mainWindow = MainWindow(testConfigPath)
	mainWindow.show()

	sys.exit( app.exec_() )