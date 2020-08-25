from PyQt5 import QtWidgets ,QtCore, QtGui
import PyQt5.QtCore as C
from final3 import Ui_MainWindow
import sys
import scipy
from scipy.io import wavfile
import os
import numpy as np
from popup import Ui_MainWindow2
from r import popWindow
from scipy.fftpack import fft
import sounddevice as sd 
from pyqtgraph import PlotWidget ,PlotItem
import pyqtgraph as pg 
import qdarkgraystyle





class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionopen.triggered.connect(lambda :self.loadFile())
        self.sliders_vector=[self.ui.verticalSlider, self.ui.verticalSlider_2 ,self.ui.verticalSlider_3,self.ui.verticalSlider_4 , self.ui.verticalSlider_5 , self.ui.verticalSlider_6 ,self.ui.verticalSlider_7,self.ui.verticalSlider_8,self.ui.verticalSlider_9, self.ui.verticalSlider_10]
        self.gains= [self.ui.gain1 ,self.ui.gain2, self.ui.gain3, self.ui.gain4,self.ui.gain5,self.ui.gain6,self.ui.gain7,self.ui.gain8,self.ui.gain9,self.ui.gain10]
        self.flag = False
        self.slider_change = False
        #for i in range(10):
            #self.sliders_vector[i].sliderReleased.connect(lambda : self.printvalue(i))
        
        
        self.ui.verticalSlider.sliderReleased.connect(lambda :self.getSliderValue(0)) 
        self.ui.verticalSlider_2.sliderReleased.connect(lambda :self.getSliderValue(1))
        self.ui.verticalSlider_3.sliderReleased.connect(lambda :self.getSliderValue(2))
        self.ui.verticalSlider_4.sliderReleased.connect(lambda :self.getSliderValue(3))
        self.ui.verticalSlider_5.sliderReleased.connect(lambda :self.getSliderValue(4))
        self.ui.verticalSlider_6.sliderReleased.connect(lambda :self.getSliderValue(5))
        self.ui.verticalSlider_7.sliderReleased.connect(lambda :self.getSliderValue(6))
        self.ui.verticalSlider_8.sliderReleased.connect(lambda :self.getSliderValue(7))
        self.ui.verticalSlider_9.sliderReleased.connect(lambda :self.getSliderValue(8))
        self.ui.verticalSlider_10.sliderReleased.connect(lambda :self.getSliderValue(9)) 
        self.ui.difference.clicked.connect(lambda : self.differencewindow())
        self.ui.radioButton.setChecked(True)  # set rectangular window mode as default
        

        self.ui.play1.clicked.connect(   lambda : self.play_original() )
        self.ui.play2.clicked.connect(   lambda : self.play_fourier()  )
        self.ui.clear.clicked.connect(lambda : self.clear_plots())
        self.ui.reset.clicked.connect(lambda : self.reset())
        self.ui.save.clicked.connect(lambda : self.save())
        self.ui.actionReset.triggered.connect(self.ui.reset.click)
        self.ui.actionClear.triggered.connect(self.ui.clear.click)
        self.ui.actionSave.triggered.connect(self.ui.save.click)
        self.ui.actionPlay1.triggered.connect(lambda :self.play_original() )
        self.ui.actionplay_new.triggered.connect(lambda :self.play_fourier() )
        self.accFlag = 0 



        self.update_sliders()        
        self.update_ui_sliders_state()  #update gains value in the UI
        self.color1 = pg.mkPen(color=(255,255,0))
        self.color2 = pg.mkPen(color=(255,0,0))



    def reset(self) : 
        for i in range(len(self.sliders_vector)) :
            self.sliders_vector[i].setValue(1)
        self.update_sliders()
        self.update_ui_sliders_state()


    def save(self) :
        self.name = QtGui.QFileDialog.getSaveFileName( self, "Save file",  os.getenv('HOME') ,"wav (*.wav)" )
        self.path = self.name[0] 
        new_file = np.copy(self.absInverse / self.absInverse.max())

        
        if self.path : 
            wavfile.write(self.path, self.fs, new_file)
        
    
    

    def update_sliders(self):

        self.sliderValue= list()

        for i in range(10) :
            self.sliderValue.append(self.sliders_vector[i].value())
            if self.sliderValue[i] <0 and self.sliderValue[i] != 0 :
                self.sliderValue[i] = 1/ np.abs(self.sliderValue[i])
        print(self.sliderValue)


    def update_ui_sliders_state(self) :
        for i in range(10) :
                if self.sliderValue[i] < 1 and self.sliderValue[i] != 0 : 
                    self.gains[i].setText(str(int(-1/self.sliderValue[i])))
                else :        
                    self.gains[i].setText(str(self.sliderValue[i]))

    
    def clear_plots(self) :
        self.ui.graphicsView.clear()
        self.ui.graphicsView_2.clear()

        


    def loadFile(self) :
        fname = QtGui.QFileDialog.getOpenFileName( self, 'choose the signal', os.getenv('HOME') ,"wav(*.wav)" )
        self.path = fname[0] 
        
        if self.path =="" :
            return
        self.flag = True

        self.fs , self.data = wavfile.read(self.path)
        print(self.data.shape[0] )
        
        self.DataFourier  =np.fft.fft(self.data)

        self.DataFourier = np.abs(self.DataFourier)

        self.DataFrequency =np.fft.fftfreq(len(self.data))

        self.copyData = self.DataFourier[:]

        print(len(self.copyData))
        while len(self.copyData)%10 != 0 :
            self.copyData = self.copyData[:-1]
        print(len(self.copyData))
        self.ui.graphicsView.setYRange(min(self.data),max(self.data)) 

        self.ui.graphicsView.plot(self.copyData , pen = self.color1) #plots wav file data in time domain ,plotted in the upper graphics view
      

        self.inverseOriginal = np.fft.ifft(self.copyData)
        self.absInverseOriginal = np.abs(self.inverseOriginal)


        self.bands = list() #creating Bands
        for i in range(10) :
            
            self.bands.append(self.copyData[int(i / 10 * len(self.copyData)) : int(min(len(self.copyData)+1,(i + 1) / 10 * len(self.copyData)))]) 
        
        self.bandContainer = self.bands[:]
        self.modificationFlags = [0,0,0,0,0,0,0,0,0,0]


        self.data_line = self.ui.graphicsView_2.plot([],[] , pen =self.color2)  
        self.update_ui_sliders_state() 

        print(len(self.bands))
        
    def hanning(self,idx,gain) :
        x = 2*len(self.bandContainer[idx])

        hanningWindow =  np.hanning(x)
    


        self.bandContainer[idx] = np.multiply(self.bandContainer[idx] ,hanningWindow[x // 2 : x + x //2]) * gain
       
        tail =len( hanningWindow[ : x // 2 ]) 
        head = len( hanningWindow[ x + x //2 : ])
        if idx == 0 :
            self.bandContainer[idx+1][:head] = np.multiply( hanningWindow[ x + x //2 : ] ,self.bandContainer[idx+1][:head] )*gain
        elif idx== 9 :
            self.bandContainer[idx-1][-tail:] = np.multiply( hanningWindow[ :x // 2 ] ,self.bandContainer[idx-1][-tail :] )*gain
        else :
            self.bandContainer[idx-1][-tail:] = np.multiply( hanningWindow[ :x // 2 ] ,self.bandContainer[idx-1][-tail :] )*gain 
            self.bandContainer[idx+1][:head] = np.multiply( hanningWindow[ x + x //2 : ] ,self.bandContainer[idx+1][:head] )*gain 


        
        
    def hamming(self,idx,gain) :

        x = 2*len(self.bandContainer[idx])

        hammingWindow =  np.hamming(x)
        self.bandContainer[idx] = np.multiply(self.bandContainer[idx] ,hammingWindow[x // 2 : x + x //2]) * gain
        tail =len( hammingWindow[ : x // 2 ]) 
        head = len( hammingWindow[ x + x //2 : ])
        if idx == 0 :
            self.bandContainer[idx+1][:head] = np.multiply( hammingWindow[ x + x //2 : ] ,self.bandContainer[idx+1][:head] )*gain
        elif idx== 9 :
            self.bandContainer[idx-1][-tail:] = np.multiply( hammingWindow[ :x // 2 ] ,self.bandContainer[idx-1][-tail :] )*gain
        else :
            self.bandContainer[idx-1][-tail:] = np.multiply( hammingWindow[ :x // 2 ] ,self.bandContainer[idx-1][-tail :] )*gain 
            self.bandContainer[idx+1][:head] = np.multiply( hammingWindow[ x + x //2 : ] ,self.bandContainer[idx+1][:head] )*gain




    def getSliderValue(self ,  index) :
        self.slider_change = True  
        self.update_sliders()   
        self.update_ui_sliders_state()
  
        
        if self.flag and self.slider_change :

            

            if self.ui.radioButton.isChecked()==True : #rectangular
                if self.modificationFlags[index] == 0 :

                    self.bandContainer[index] = np.multiply(self.bandContainer[index],self.sliderValue[index]) 
                    self.modificationFlags[index] = 1  

                else :
                    self.bandContainer[index] = self.bands[index]
                    self.bandContainer[index] = np.multiply(self.bandContainer[index],self.sliderValue[index])

            elif self.ui.radioButton_2.isChecked()==True : #hanning
                if self.modificationFlags[index] == 0 :

                    self.hanning(index,self.sliderValue[index])
                    self.modificationFlags[index] = 1  

                else :
                    self.bandContainer[index] = self.bands[index]
                    self.hanning(index,self.sliderValue[index])

            elif self.ui.radioButton_3.isChecked()==True :#hamming
                if self.modificationFlags[index] == 0 :

                    self.hamming(index,self.sliderValue[index])
                    self.modificationFlags[index] = 1  

                else :
                    self.bandContainer[index] = self.bands[index]
                    self.hamming(index,self.sliderValue[index])

            for i in range(len(self.bandContainer) ):

                #print(self.bandContainer[i][0:2])
                print( self.bandContainer[i][-2:])
            self.datay= list()
            for i in range(10):
                for j in self.bandContainer[i]:
                    self.datay.append(j)
            self.update_sliders()
            self.update_ui_sliders_state()
            #self.bandContainer= self.bands[:]

            
            self.data_line.setData(self.DataFrequency[range(len(self.datay))], self.datay) 
            self.ui.graphicsView_2.setYRange(min(self.datay),max(self.datay))   
            self.ui.graphicsView_2.plot(self.DataFrequency[range(len(self.datay))], self.datay,pen= self.color2)

            self.inverse = np.fft.ifft(self.datay)
            self.absInverse = np.abs(self.inverse)
            self.ui.graphicsView.plot(self.absInverse , pen = self.color1)

            self.update_ui_sliders_state() 

                        

    def play_original(self) :
        
        sd.play( self.copyData, self.fs)


    def play_fourier(self) :
     
        sd.play( self.absInverse / self.absInverse.max(),self.fs)

 

        

    def differencewindow(self): 
        if self.flag and self.slider_change :
           self.window = popWindow()
           self.diff_freq =   self.datay -  self.copyData
           self.diff_Time =  self.absInverse  - self.absInverseOriginal 
           color3 = pg.mkPen(color=(0,240,0))
           color4 = pg.mkPen(color=(150,0,150))
         
           self.window.ui.graphicsView_2.setYRange(min(self.diff_Time)/2,max(self.diff_Time)/2)   

           self.window.ui.graphicsView.plot(self.diff_freq,pen= color3) 
           self.window.ui.graphicsView_2.plot(self.diff_Time,pen=color4 ) 

           self.window.show()

    


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__))) # to load the directory folder

    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()