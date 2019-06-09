#!/usr/bin/env python


import sys
import os

import rospy
from sensor_msgs.msg import Image

import cv2
import numpy as np

from utility.imageToMessage import cvtImageMessageToCVImage


from PyQt4 import QtGui, QtCore


class Camera2( QtCore.QThread ):
	
	imageSignal = QtCore.pyqtSignal( object )

	def __init__( self ):

		super( Camera2, self ).__init__()
		
		rospy.init_node( "Camera2" )
		rospy.Subscriber( "/vision_manager/cranial_nerve_ii_topic", Image, self.cameraCallback, queue_size=1 )

		# freq = rospy.get_param( "/vision_manager/cranial_nerve_ii_frquency" )
		self.rate = rospy.Rate( 60 )

		self.frame = np.zeros( (480,640,3),dtype=np.uint8 )

	def cameraCallback( self, msg ):
		
		self.frame = cvtImageMessageToCVImage( msg )

		# self.frame = cv2.cvtColor( self.frame, cv2.COLOR_BGR2RGB )

	def read( self ):
		return self.frame

	def run( self ):
		
		rospy.loginfo( "Enter camera node." )
		while True:				
			img = self.read()

			rgbImage = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
			
			self.imageSignal.emit( rgbImage )

			self.rate.sleep()
