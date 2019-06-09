#!/usr/bin/env python

import os
import sys

import time
import threading

from PyQt4 import QtCore
from PyQt4 import QtGui

class Window( QtGui.QWidget ):

    def __init__( self ):
        super( Window, self ).__init__()

        self.button = QtGui.QPushButton( "Clicked" )
        self.button.clicked.connect( self.buttonCallback )

        self.label = QtGui.QLabel()
        self.label.setAlignment( QtCore.Qt.AlignCenter )

        self.vBox = QtGui.QVBoxLayout()
        self.vBox.addWidget( self.label )
        self.vBox.addWidget( self.button )

        self.setLayout( self.vBox )

        # self.thread = SimpleThread( 1 )
        # self.thread.start()

        self.thread = SimpleQtThread( 1 )
        self.thread.signal.connect( self.signalCallback )
        self.thread.start()

    def buttonCallback( self ):

        print "Button is clicked"
        self.label.setText( "Clear" )

    def signalCallback( self,data ):
        self.label.setText( "Add : {}".format( data ) )



class SimpleThread( threading.Thread ):

    def __init__( self, threadID ):
        
        super( SimpleThread, self ).__init__()

        self.threadID = threadID

    def run( self ):

        print "Start thread : {}".format( self.threadID )
        for i in xrange( 100 ):
            print "Process something"
            time.sleep( 1 )
        

class SimpleQtThread( QtCore.QThread ):

    #   Define signal
    signal = QtCore.pyqtSignal( object )

    def __init__( self, threadID ):

        super( SimpleQtThread, self ).__init__()

    def run( self ):

        for i in xrange( 100 ):
            print "Process something : emit index"
            time.sleep( 1 )
            self.signal.emit( i )



if __name__ == "__main__":
    
    app = QtGui.QApplication( sys.argv )

    window = Window()
    window.show()

    sys.exit( app.exec_() )