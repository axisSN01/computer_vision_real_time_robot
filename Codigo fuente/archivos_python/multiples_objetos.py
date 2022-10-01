#-*- coding: utf-8 -*-

import cv
#-----------------------------------------------------------

def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)

#-----------------------------------------------------------

def multiples_objetos(hist,frame,dic,track_window,(Hmin,Hmax,Smin,Smax)):
    if not is_rect_nonzero(track_window):
        cv.Smooth(frame, frame, cv.CV_GAUSSIAN, 3, 0)
        imghsv=cv.CreateImage(cv.GetSize(frame),8,3)
        cv.CvtColor(frame,imghsv,cv.CV_BGR2HSV)
        color_mask1 = cv.CreateImage(cv.GetSize(frame), 8, 1)
        [_,_,_,_, Hmin, Hmax, Smin, Smax]=BW_hist(hist)

        if Smin>Smax:
            cv.InRangeS(imghsv, cv.Scalar(Hmin,0,0), cv.Scalar(Hmax,255,255), color_mask1) # bw no es parejo
        else:cv.InRangeS(imghsv, cv.Scalar(Hmin,0,0), cv.Scalar(Hmax,255,255), color_mask1)
                #encontrar contornos
        #cv.SaveImage("mask_virgen.jpg",color_mask1)
        cv.Erode(color_mask1,color_mask1,None,dic["Erode"])# erode muy grande
        cv.Dilate(color_mask1,color_mask1,None,dic["Dilate"]) # dilate muy grande
        #cv.SaveImage("mask_conEyD.jpg",color_mask1)
        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(color_mask1, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        points = []	
        areas = []
        ret_point=(0,0,0,0)
        while contour: # dibujar rectangulos
            bound_rect = cv.BoundingRect(list(contour))
            Area= cv.ContourArea(contour)
            areas.append(Area)
            contour = contour.h_next()
            pt1 = (bound_rect[0], bound_rect[1])
            pt2 =(bound_rect[2], bound_rect[3])
            points.append([pt1,pt2])
            cv.Circle(frame,(bound_rect[0]+bound_rect[2]/2,bound_rect[1]+bound_rect[3]/2),4,[0,0,255],-1)

        AreaMin=dic["t_min"]*1600.0/(dic["lineablanca"]**2)   # valores calibrados Amin *( px_lineaBlanca**2 )/(cm_Lblanca**2)=Area en px2
        AreaMax=dic["t_max"]*1600.0/(dic["lineablanca"]**2)       
        if dic["crit"]==0:          # criterio 0, menor a mayor
            AreaAux=AreaMax
            for i in range(0,len(areas)):
                if areas[i]<=AreaMax and areas[i]>=AreaMin:         # rango de areas
                    if areas[i]<=AreaAux:
                        ret_point=(points[i][0][0],points[i][0][1],points[i][1][0],points[i][1][1])
                        AreaAux=areas[i]

        if dic["crit"]==1:          # criterio 1, mayor a menor
            AreaAux=AreaMin        
            for i in range(0,len(areas)):
                if areas[i]<=AreaMax and areas[i]>=AreaMin:
                    if areas[i]>=AreaAux:
                        ret_point=(points[i][0][0],points[i][0][1],points[i][1][0],points[i][1][1])
                        AreaAux=areas[i]

        if dic["crit"]==2:          # criterio 2, primero en aparecer
            #ret_point=(points[0][0][0],points[0][0][1],points[0][1][0],points[0][1][1])
            for i in range(0,len(areas)):
                if areas[i]<=AreaMax and areas[i]>=AreaMin:
                    ret_point=(points[i][0][0],points[i][0][1],points[i][1][0],points[i][1][1])

        centroid_x=ret_point[0]+ret_point[2]/2    # x
        centroid_y=ret_point[1]+ret_point[3]/2       # y


    elif is_rect_nonzero(track_window):
        #--------------------------------------------------------------------------------
        # con el track_window de t-1, hago AND y dejo solo track_window + delta, para que busque el camshift.evito confuciones de
        # camshift 
        #--------------------------------------------------------------------------------
        cv.Smooth(frame, frame, cv.CV_GAUSSIAN, 3, 0)
        mask=cv.CreateImage(cv.GetSize(frame), 8, 3)
        # estructura de track_window:
        #cv.EllipseBox( mask, track_window, cv.CV_RGB(255,255,255), -1, cv.CV_AA, 0 )
        x0=int(track_window[0])
        y0=int(track_window[1])
        x1=int(track_window[0]+track_window[2])
        y1=int(track_window[1]+track_window[3])
        cv.Rectangle(mask,(x0,y0),(x1,y1),cv.CV_RGB(255,255,255),-1)
        cv.And(frame,mask,mask) # y con esto queda el cuadrito solo
        #cv.SaveImage("framAND.jpg",mask)        
        #--------------------------------------------------------------------------------        
        #   con camshift obtengo el nuevo centro del obejto, y su nueva track_window
        #--------------------------------------------------------------------------------
        imghsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(mask, imghsv, cv.CV_BGR2HSV)
        color_mask=cv.CreateImage(cv.GetSize(frame), 8, 1)
        #hue = cv.CreateImage(cv.GetSize(frame), 8, 1)
        #Sat = cv.CreateImage(cv.GetSize(frame), 8, 1)
        #Val = cv.CreateImage(cv.GetSize(frame), 8, 1)
        #cv.Split(hsv, hue, Sat, Val, None)
        #cv.SaveImage("hue.jpg",hue)
        #cv.SaveImage("sat.jpg",Sat)
        #cv.SaveImage("val.jpg",Val)        
        #Compute back projection
        #backproject = cv.CreateImage(cv.GetSize(frame), 8, 1)
        # Run the cam-shift
        #cv.CalcArrBackProject( [Val], backproject, hist )
        #cv.Threshold(backproject,backproject,25,255,cv.CV_THRESH_BINARY)
        if Smin>Smax:
            cv.InRangeS(imghsv, cv.Scalar(Hmin,0,0), cv.Scalar(Hmax,255,255), color_mask) # bw no es parejo
        else:cv.InRangeS(imghsv, cv.Scalar(Hmin,0,0), cv.Scalar(Hmax,255,255), color_mask)        
        cv.Erode(color_mask,color_mask,None,dic["Erode"]) 
        cv.Dilate(color_mask,color_mask,None,dic["Dilate"])
        #cv.SaveImage("color_mask.jpg",color_mask)
        #storage = cv.CreateMemStorage(0)
        #contour = cv.FindContours(color_mask, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)	        

        #PointArray2D32f = cv.CreateMat(1, len(contour), cv.CV_32FC2)
	    #for (i, (x, y)) in enumerate(contour):
            #PointArray2D32f[0, i] = (x, y)
        #track_box=cv.FitEllipse2(PointArray2D32f) # aca tiene q haber si o si un solo contorno
        # track_box : ((xcentro,ycentro),(x_length,y_length),angulo_rot)
        # area: pix**2
        # rect: (x0,y0,x_lenght,y_lenght)
        #track_window = rect
        #ret_point = cv.BoundingRect(list(contour))
        #cv.DrawContours(frame, contour, [255,0,0], [0,0,0], 0)
        #ret_point= (track_box[0][0]-track_box[1][0]/2,track_box[0][1]-track_box[1][1]/2,track_box[1][0],track_box[1][1])
        crit = ( cv.CV_TERMCRIT_EPS | cv.CV_TERMCRIT_ITER, 10, 10)
        (_,(area, _, rect),track_box )= cv.CamShift(color_mask,track_window, crit)
        ret_point=rect
        track_window=ret_point
        cv.EllipseBox( frame, track_box, cv.CV_RGB(255,0,0), 1, cv.CV_AA, 0 )
        centroid_x=int(ret_point[0]+ret_point[2]/2)   # x
        centroid_y=int(ret_point[1]+ret_point[3]/2)       # y
        cv.Circle(frame,(centroid_x,centroid_y),4,[0,0,255],-1)

    if centroid_x<dic["rectangulo"][2] and centroid_x>dic["rectangulo"][0] and centroid_y<dic["rectangulo"][3] and centroid_y>dic["rectangulo"][1]: 
        return ret_point, frame, (centroid_x,centroid_y), (Hmin,Hmax,Smin,Smax)
    else: return

#-----------------------------------------------------------
def BW_hist(hist):
    (min_val, max_val, X_min, X_max) = cv.GetMinMaxHistValue( hist)
    x_max=X_max[0]
    x_min=X_min[0]  
    i=x_max
    while hist.bins[i]>0.01*max_val and i<254:  #max_val>=hist.bins[i] and . aca era 178.ahora 254
        i=i+1                        
        bw_x_max=i # busco ancho de banda en H(matiz)
    i=x_max
    while hist.bins[i]>0.01*max_val:  #max_val>=hist.bins[i] and 
        i=i-1                        
        bw_x_min=i  
    Hmin=bw_x_min#*255/179#-75   # mapeo los valores en x, de 0-180 a 0-255, offset de 50
    Hmax=bw_x_max#*255/179
    Smin=hist.bins[bw_x_min]#*255/max_val   # aca no es 255 porque ya viene normalizado
    Smax=hist.bins[x_max]#*255/max_val   # rango de intensidad del color

    return [bw_x_min, bw_x_max, 255,255, Hmin, Hmax, Smin, Smax]    # pongo v_min y v_max a maximo, ventana cuadrada
