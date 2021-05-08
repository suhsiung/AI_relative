import cv2,os
from PIL import Image
#########################################################  
picName="pic001.jpg"     ##設定影像檔名
picPath="picIn"         ##設定影像儲存檔案夾名
picOutPath="picOut"     ##設定影像結果檔案夾名
#########################################################
###   顯示挑選圖片:
cv2.namedWindow("MyPicture", cv2.WINDOW_NORMAL)
picx=cv2.imread(picPath+"/"+picName)
gray = cv2.cvtColor(picx, cv2.COLOR_RGB2GRAY)
cv2.imshow("MyPicture",picx)
cv2.waitKey(0)                  ## 等待
cv2.destroyAllWindows()         ##關閉所有視窗
###   人臉辨識   ###
picx=cv2.imread(picPath+"/"+picName)
faceDetector=cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
picFaces=faceDetector.detectMultiScale(gray,scaleFactor=1.5,\
                                    minNeighbors=4,minSize=(70,70),
                                    maxSize=(500,500))
print("在圖中辨識出人臉的個數為:",len(picFaces),"位")
###  顯示辨識後的圖片(加人臉框):
##將所有發現的人臉用方框標註:
for (x,y,w,h) in picFaces:
    cv2.rectangle(picx,(x,y),(x+w,y+h),(255,0,0),2)
##在影像左上角標註偵測發現的人數:
cv2.rectangle(picx,(5,5),(150,30),(0,255,255),-1)
cv2.putText(picx,"Finding "+str(len(picFaces))+ " face(s)",
            (10,20),cv2.FONT_ITALIC,0.5,(255,0,0),2)
## 使用OpenCV視窗顯示影像: cv2.imshow(視窗名稱,影像物件)
cv2.namedWindow("MyPicture", cv2.WINDOW_NORMAL)
cv2.imshow("MyPicture",picx)
cv2.waitKey(0)                  ## 等待
cv2.destroyAllWindows()         ##關閉所有視窗
###  將偵測發現的臉部存檔:  ###
## 清空 picOut 檔案夾:
DATA_DIR = "picOut"                                  # 設定欲清空的膽案夾名稱
removeFiles=os.listdir(DATA_DIR)                     # 找出該檔案夾內的所有檔案名稱
for i in removeFiles: os.remove(DATA_DIR + '/' + i)  # 執行刪除檔案工作
##  執行臉部存檔:  
imgx=Image.open(picPath+"/"+picName)
num=1
for (x,y,w,h) in picFaces:
    filename="face" + str(num) + ".jpg"
    imgxCrop=imgx.crop((x,y,x+w,y+h))
    imgxResize=imgxCrop.resize((150,150),Image.ANTIALIAS)
    imgxResize.save(picOutPath+"/"+filename)
    num+=1
#########################################################    
    
    
    
    
    
    
    
    
    
    