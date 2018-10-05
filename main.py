from PyQt5.QtGui import QPalette, QKeySequence, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLineEdit,
                            QPushButton, QSizePolicy, QSlider, QMessageBox, QStyle, QVBoxLayout,  
                            QWidget, QShortcut, QFormLayout, QDialog)
import os
import re
try:
    import subprocess
    from subprocess import run
except:
    pass
try:
    import subprocess32
    from subprocess32 import run
except:
    pass
from builtins import str

class VideoPlayer(QWidget):

    def __init__(self, aPath, parent=None):
        super(VideoPlayer, self).__init__(parent)
        
        #self.setAttribute(Qt.WA_NoSystemBackground, True)
        
        self.colorDialog = None
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(80)
        self.videoWidget = QVideoWidget(self)
        
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setEnabled(False)
        self.lbl.setFixedWidth(60)
        self.lbl.setUpdatesEnabled(True)
        #self.lbl.setStyleSheet(stylesheet(self))
        
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setEnabled(False)
        self.elbl.setFixedWidth(60)
        self.elbl.setUpdatesEnabled(True)
        #self.elbl.setStyleSheet(stylesheet(self))
        
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(32)
        #self.playButton.setStyleSheet("background-color: black")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        ### pointA button
        self.apointButton = QPushButton()
        self.apointButton.setEnabled(False)
        self.apointButton.setFixedWidth(32)
        #self.apointButton.setStyleSheet("background-color: black")
        self.apointButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.apointButton.clicked.connect(self.setPointA)
        
        ### pointB button
        self.bpointButton = QPushButton()
        self.bpointButton.setEnabled(False)
        self.bpointButton.setFixedWidth(32)
        #self.bpointButton.setStyleSheet("background-color: black")
        self.bpointButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.bpointButton.clicked.connect(self.setPointB)
        
        ### cut button
        self.cutButton = QPushButton()
        self.cutButton.setEnabled(False)
        self.cutButton.setFixedWidth(32)
        self.cutButton.setIcon(self.style().standardIcon(QStyle.SP_DriveFDIcon))
        self.cutButton.clicked.connect(self.cut)
        
        self.positionSlider = QSlider(Qt.Horizontal,self)
        self.positionSlider.setStyleSheet(stylesheet(self))
        self.positionSlider.setRange(0,100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.sliderMoved.connect(self.handleLabel)
        self.positionSlider.setSingleStep(2)
        self.positionSlider.setPageStep(20)
        #self.positionSlider.setAttribute(Qt.WA_NoSystemBackground, True)
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(5,0,5,0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.apointButton)
        controlLayout.addWidget(self.bpointButton)
        controlLayout.addWidget(self.cutButton)
        controlLayout.addWidget(self.lbl)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.elbl)
        
        layout0 = QVBoxLayout()
        layout0.setContentsMargins(0,0,0,0)
        layout0.addWidget(self.videoWidget)
        layout0.addLayout(controlLayout)
        
        self.setLayout(layout0)
        
        self.widescreen = True
        
        self.setAcceptDrops(True)
        self.setWindowTitle("QT5 Player")
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(300,200,400,290)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested[QtCore.QPoint].connect(self.contextMenuRequested)
        #self.hideSlider()
        self.show()
        #self.playFromURL()
        
        ### shortcuts ###
        self.shortcut = QShortcut(QKeySequence('q'), self)
        self.shortcut.activated.connect(self.handleQuit)
        self.shortcut = QShortcut(QKeySequence('o'), self)
        self.shortcut.activated.connect(self.openFile)
        self.shortcut = QShortcut(QKeySequence(' '), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence('s'), self)
        self.shortcut.activated.connect(self.toggleSlider)
        self.shortcut = QShortcut(QKeySequence('v'), self)
        self.shortcut.activated.connect(self.setPointA)
        self.shortcut = QShortcut(QKeySequence('b'), self)
        self.shortcut.activated.connect(self.setPointB)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier+Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider10)
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier+Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider10)
        
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.positionChanged.connect(self.handleLabel)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        self.apoint = 0
        self.bpoint = 0
        self.inputfile = 0
        self.outputfile = 0
    
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Movie', QDir.homePath()+'/Desktop', 'Videos (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v)')
        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")
            print(fileName)
            self.inputfile = fileName

    
    def getclipFileName(self):
        clipFileName = QFileDialog.getSaveFileName(self, 'Save Clip', QDir.homePath()+'/Desktop', 'all files(*.*)')
        return clipFileName
            
    #def playFromURL(self):
    
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
    
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())
    
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    ### cut point A function
    def setPointA(self):
        self.apoint = self.time.toString()
        print('A Point ' + self.apoint)
        
    ### cut point B function
    def setPointB(self):
        self.play()
        self.bpoint = self.time.toString()
        print('B Point ' + self.bpoint)
        
    ### cut
    def cut(self):
        #self.outputfile = self.getclipFileName()[0]
        print(self.inputfile)
        print(self.outputfile)
        length = self.lengthCalculation(self.apoint, self.bpoint)
        inputfile0 = re.sub(' ','\ ',self.inputfile)
        outputfile0 = inputfile0[:-4]+'__'+self.apoint+'__'+self.bpoint+inputfile0[-4:]
        outputfile0 = re.sub(':','_',outputfile0)
        self.outputfile =outputfile0
        command = "ffmpeg -n -ss "+self.apoint+" -i "+inputfile0+" -c copy -t "+length+" "+self.outputfile
        print(command)
        run(command, shell=True)
    
    ### cut length calculation
    def twodigi(self,str0):
        if len(str0) == 1:
            str0 = '0'+str0
        return str0
    
    def lengthCalculation(self, start, end):
        start_s = int(start[:2])*3600+int(start[3:5])*60+int(start[6:])
        print(start_s)
        end_s = int(end[:2])*3600+int(end[3:5])*60+int(end[6:])
        print(end_s)
        length_s = end_s - start_s
        print(length_s)
        hr = self.twodigi(str(length_s//3600))
        mn = self.twodigi(str((length_s%3600)//60))
        sc = self.twodigi(str(length_s%60))
        length = hr+':'+mn+':'+sc
        print(length)
        return length
        
    
    def handleError(self):
        self.playButton.setEnabled(False)
        self.apointButton.setEnabled(False)
        self.bpointButton.setEnabled(False)
        self.cutButton.setEnabled(False)
        print("Error: " + self.mediaPlayer.errorString())
    
    def handleQuit(self):
        self.mediaPlayer.stop()
        print('Quit.')
        app.quit()
    
    def contextMenuRequested(self, point):
        menu = QtWidgets.QMenu()
        actionFile = menu.addAction('Open File (o)')
        actionFile.triggered.connect(self.openFile)
        
        actionToggle = menu.addAction('show / hide Slider (s)')
        actionToggle.triggered.connect(self.toggleSlider)
        
        action169 = menu.addAction('16 : 9')
        action169.triggered.connect(self.screen169)
        
        action43 = menu.addAction('4 : 3')
        action43.triggered.connect(self.screen43)
        
        actionQuit = menu.addAction('Exit (q)')
        actionQuit.triggered.connect(self.handleQuit)
        
        menu.exec_(self.mapToGlobal(point))
    
    def wheelEvent(self, event):
        mwidth = self.frameGeometry().width()
        #mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = event.angleDelta().y() / 5
        if self.widescreen == True:
            self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.778) 
        else:
            self.setGeometry(mleft, mtop, mwidth + mscale, (mwidth + mscale) / 1.33)
    
    def screen169(self):
        self.widescreen = True
        mwidth = self.frameGeometry().width()
        #mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, mwidth/mratio)
    
    def screen43(self):
        self.widescreen = False
        mwidth = self.frameGeometry().width()
        #mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)
    
    def handleFullscreen(self):
        pass
    
    def handleInfo(self):
        pass
    
    def toggleSlider(self):
        if self.positionSlider.isVisible():
            self.hideSlider()
        else:
            self.showSlider()
    
    def hideSlider(self):
        self.playButton.hide()
        self.lbl.hide()
        self.positionSlider.hide()
        self.elbl.hide()
        mwidth = self.frameGeometry().width()
        #mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        if self.widescreen == True:
            self.setGeometry(mleft, mtop, mwidth, mwidth / 1.778) 
        else:
            self.setGeometry(mleft, mtop, mwidth, mwidth / 1.33)
    
    def showSlider(self):
        self.playButton.show()
        self.lbl.show()
        self.positionSlider.show()
        self.elbl.show()
        mwidth = self.frameGeometry().width()
        #mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        self.positionSlider.setFocus()
        if self.widescreen == True:
            self.setGeometry(mleft, mtop, mwidth, mwidth / 1.55) 
        else:
            self.setGeometry(mleft, mtop, mwidth, mwidth / 1.33)
    
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position()+100*60)
    
    def forwardSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position()+250*60)
    
    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position()-100*60)
    
    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position()-250*60)
    
    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume()+10)
        
    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume()-10)
    '''
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            #self.move(event.globalPos() - QPoint(self.frameGeometry().width() / 2, self.frameGeometry().height() / 2))
            self.move(event.globalPos() - QPoint(self.geometry().left(),self.geometry().top()))
            event.accept()
    '''
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        elif event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            f = str(event.mimeData().urls()[0].toLocalFile())
            self.loadFilm(f)
            self.inputfile = f
        elif event.mimeData().hasText():
            f = str(event.mimeData().text())
            self.mediaPlayer.setMedia(QMediaContent(QUrl(f)))
            self.inputfile = f
            self.mediaPlayer.play() 
    
    def loadFilm(self, f):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
        self.playButton.setEnabled(True)
        self.apointButton.setEnabled(True)
        self.bpointButton.setEnabled(True)
        self.cutButton.setEnabled(True)
        self.mediaPlayer.play()
        #print(str(self.mediaPlayer.media().canonicalResource().resolution()))
    
    def openFileAtStart(self, filelist):
        matching = [s for s in filelist if '.myformat'  in s]
        if len(matching) > 0:
            self.loadFilm(matching)
    
    def handleLabel(self):
        self.lbl.clear()
        mtime = QTime(0,0,0,0)
        self.time = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(self.time.toString())

def stylesheet(self):
    return """
QSlider::handle:horizontal 
{
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #333, stop:1 #555555);
width: 14px;
border-radius: 0px;
}
QSlider::groove:horizontal {
border: 1px solid #444;
height: 10px;
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000, stop:1 #222222);
}
QLineEdit
{
background: black;
color: #585858;
border: 0px solid #076100;
font-size: 11px;
font-weight: bold;
font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
    """

if __name__ == '__main__':
    
    import sys
    app = QApplication(sys.argv)
    player = VideoPlayer('')
    if len(sys.argv) > 1:
        print(sys.argv[1])
        player.loadFilm(sys.argv[1])
    player.resize(720,480)
        
sys.exit(app.exec_())