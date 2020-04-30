#importing dependencies
import os
import sys
import pandas as pd
import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore, QtGui 
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

#defining main class for window
class Form(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        """"" Loading the UI File """
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "Try2.ui"),self) 
        """ Setting Multimedia player to play video"""
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        """ Setting up the Video Widget, Slider and Layout"""
        self.player.setVideoOutput(self.ui.widget)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(QtGui.QHBoxLayout())

        self.slider.show()
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)
        """ Slider position and duratio synchronization"""
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        
        imv = pg.ImageView()  
        self.widget.layout().addWidget(imv)

        self.actionOpen.setStatusTip('Open movie')
        """ Triggering File Open when File button is clicked"""
        self.actionOpen.triggered.connect(self.openFile)

        self.show()
    
    def positionChanged(self, position):
        """Slider position change manually """
        self.slider.setValue(position)
    
    def play(self):
        """ Play video on the video widget """
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    """ Duration change attachment from slider to video """
    def durationChanged(self, duration):
        self.slider.setRange(0, duration)
        global vidlen
        vidlen = duration
        print('duration')
        print(vidlen)
    
    def setPosition(self, position):
        """ Setting the position and play"""
        self.player.setPosition(position)
        self.player.play()
        """Synchronize the signal slider when video slider is moved"""        
        #print(position)
        p= ((position/vidlen)*column)
        p=int(p)
        #print(p)
        self.graphicsView.setCurrentIndex(p)
        #print(self.graphicsView.currentIndex)


    def setCurrentIndex(self, ind):
        """Set the currently displayed frame index"""
        self.currentIndex = np.clip(ind, 0, self.getProcessedImage().shape[self.axes['t']]-1)
        print("here")
        self.updateImage()
        self.ignoreTimeLine = True
        self.timeLine.setValue(self.tVals[self.currentIndex])
        self.ignoreTimeLine = False

    def openFile(self):

        """ To open folder and setting up the respective files"""
        dir_ = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        fileName = f'{dir_}/video.avi'
        dataName = f'{dir_}/signal.csv'

        if fileName != '' and dataName != '':

            
            self.player.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            """Open the signal file"""  
            data = pd.read_csv(dataName,header=None)
            test_read = data.values
            
            """Pre-Process the signal file"""
            a = np.transpose(test_read)

            #print(test_read)
            #print(test_read.shape)
            global column
            column = test_read.shape[1]
            print(column)
            query=a.reshape(column,118,48)
            query=query.transpose(0, 2, 1)  
            
            """Pass the signal data to the Widget""" 
            self.graphicsView.show()
            self.graphicsView.setImage(query)
            
            """Set the color, threshold and auto play or signal data"""    
            self.graphicsView.setPredefinedGradient('flame')    
            self.graphicsView.setLevels(0,80)
            self.graphicsView.play(1)            
            self.player.play()         
                
        

if __name__ == '__main__':

    """Start the application"""    
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec())