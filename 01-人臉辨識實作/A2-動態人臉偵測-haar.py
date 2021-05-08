
import cv2,os
from PIL import Image
face_cascade=cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
cv2.namedWindow("VideoImg")
cap=cv2.VideoCapture(0)
while (cap.isOpened()):
    ret,picx=cap.read()
    picfaces=face_cascade.detectMultiScale(picx,scaleFactor=1.1,\
                                    minNeighbors=3,minSize=(20,20),
                                    maxSize=(580,580))
    for (x,y,w,h) in picfaces:
        cv2.rectangle(picx,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow("VideoImg",picx)
    if ret == True:
        key=cv2.waitKey(200)
        if key ==ord("a") or key ==ord("A"):
            ## 清空 picOut 檔案夾:
            DATA_DIR = "picOut"                                  # 設定欲清空的膽案夾名稱
            removeFiles=os.listdir(DATA_DIR)                     # 找出該檔案夾內的所有檔案名稱
            for i in removeFiles: os.remove(DATA_DIR + '/' + i)  # 執行刪除檔案工作
            ##  執行臉部存檔:  
            num=1
            cv2.imwrite("./picOut/photo.jpg",picx)
            imgx=Image.open("./picOut/photo.jpg")
            for (x,y,w,h) in picfaces:
                filename="face" + str(num) + ".jpg"
                imgxCrop=imgx.crop((x,y,x+w,y+h))
                imgxResize=imgxCrop.resize((150,150),Image.ANTIALIAS)
                imgxResize.save(DATA_DIR+"/"+filename)
                num += 1
            ######################################################### 
            
            break
cap.release()
cv2.destroyAllWindows() 