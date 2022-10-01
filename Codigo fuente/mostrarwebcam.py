#! /usr/bin/env python 
 
import cv

class webcam: 
    
    def __init__(self): 
        cv.NamedWindow( "Camara", 1 )
        c=input("")
        self.capture = cv.CaptureFromCAM(c) 
        
    def run(self): 
        while True: 
            img = cv.QueryFrame( self.capture ) 
            cv.ShowImage("Camara", img) 
            
            if cv.WaitKey(10) == 27: 
                break 
                
if __name__=="__main__": 
    cam = webcam() 
    cam.run() 
