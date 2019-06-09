#!/usr/bin/env python


import os
import sys

import cv2
import numpy as np

from PyQt4 import QtGui, QtCore

from camera import Camera2
from slider_widget import Slider

from config_generator import getConfigDict, setNewValueToConfigColor, getConfigValue, saveConfig


class ImageLabel( QtGui.QLabel ):
	""" FOR Renderer only! """

	def __init__( self, sliderBar ):
		
		#   call super class of label
		super( ImageLabel, self ).__init__()

		self.imageThread = Camera2()
		self.imageThread.imageSignal.connect( self.signalCallback )
		self.imageThread.start()

		self.slider = sliderBar

		self.upperBoundArray = np.array( [ 0, 0, 0 ] )
		self.lowerBoundArray = np.array( [ 0, 0, 0 ] )

	def signalCallback( self, data ):
		
		self.setImageLabel( data )

	def setImageLabel( self, image ):

		#
		#	HSV stuff
		#

		self.getLowerAndUpperBound()

		hsvImage = cv2.cvtColor( image, cv2.COLOR_RGB2HSV )
		mask = cv2.inRange( hsvImage, self.lowerBoundArray, self.upperBoundArray )
		resImage = cv2.bitwise_and( image, image, mask=mask )

		#	Get information of image
		height, width, channel = image.shape
		bytePerRow = image.strides[ 0 ]

		qImage = QtGui.QImage( resImage.data, width, height, bytePerRow, QtGui.QImage.Format_RGB888 )

		#   create pixmap by QImage object
		self.pixmap = QtGui.QPixmap( qImage )

		#	set pixmap to image label
		self.setPixmap( self.pixmap )

	def getLowerAndUpperBound( self ):

		hMax, sMax, vMax, hMin, sMin, vMin = self.slider.getValue()

		self.lowerBoundArray = np.array( [ hMin, sMin, vMin ] )
		self.upperBoundArray = np.array( [ hMax, sMax, vMax ] )

class ImageWidget( QtGui.QWidget ):

	def __init__( self, configPathStr ):

		super( ImageWidget, self ).__init__()
		
		#	Get config to dict
		self.configDict = getConfigDict( path = configPathStr )

		self.colorComboBox = QtGui.QComboBox()
		self.colorComboBox.addItems( self.configDict[ "ColorDefinitions" ].keys() )
		self.colorComboBox.currentIndexChanged.connect( self.colorComboBoxCallback )

		self.slider = Slider( *getConfigValue( self.configDict[ "ColorDefinitions" ], self.configDict[ "ColorDefinitions" ].keys()[ 0 ] ) )

		self.imageLabel = ImageLabel( self.slider )

		self.submitButton = QtGui.QPushButton( "Submit" )
		self.submitButton.clicked.connect( self.submitButtonCallback )

		self.layout = QtGui.QVBoxLayout()
		
		self.layout.addWidget( self.imageLabel )
		self.layout.addWidget( self.colorComboBox )
		self.layout.addWidget( self.slider )
		self.layout.addWidget( self.submitButton )

		self.setLayout( self.layout )
	
	def submitButtonCallback( self ):
		
		hMax, sMax, vMax, hMin, sMin, vMin = self.slider.getValue()

		currentKey = str( self.colorComboBox.currentText() )
		setNewValueToConfigColor( self.configDict[ "ColorDefinitions" ], currentKey, H_max=hMax, H_min=hMin, S_max=sMax, S_min=sMin, V_max=vMax, V_min=vMin )

		print "Commit!"

	def colorComboBoxCallback( self ):
		
		#	Get keys
		currentKey = str( self.colorComboBox.currentText() )
		self.slider.setValue( *getConfigValue( self.configDict[ "ColorDefinitions" ], currentKey ) )

	def saveConfig( self, savePathStr ):

		saveConfig( self.configDict, savePathStr=savePathStr )

	def loadConfig( self, configPathStr ):

		self.configDict = getConfigDict( path = configPathStr )
	
	def updateUI( self ):
		
		currentKey = str( self.colorComboBox.currentText() )
		self.slider.setValue( *getConfigValue( self.configDict[ "ColorDefinitions" ], currentKey ) )
		


if __name__ == "__main__":

	app = QtGui.QApplication( sys.argv )

	testConfigPath = "/home/neverholiday/work/ros_ws/src/pyxis/src/config_generator/config.ini"

	imageWindow = ImageWidget( testConfigPath )
	imageWindow.show()

	sys.exit( app.exec_() )