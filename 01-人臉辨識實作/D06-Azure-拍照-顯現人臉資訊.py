## 填寫部分 ：   ###################################################################
groupName='group01'          ## '填入群組名稱-英文,例如: group01'    
base ='https://suface3.cognitiveservices.azure.com/face/v1.0'              ## '填入端點'   
key = '5e73a46ec71a45a0b1d09100f4447324'              # 
####################################################################################

## 安裝 SpeechRecognition套件：
## !pip install SpeechRecognition
## 安裝使用麥克風套件: PyAudio
## !pip install PyAudio
##安裝 gTTS 套件:
## !pip install gTTS    #google_Text_To_Speech
## 安裝 pygame 套件: 負責處理聲音的物件，在此作為播放聲音
## !pip install pygame
## !pip install hanziconv

import DA_000_subot_func as suaia
import DB_000_subot_func as suaib
import operator,cv2

xbase = base
xkey = key                              
xgid = groupName
####################################################################################

ximg=suaia.subot_faceShot2()
xheaders_stream = {'Ocp-Apim-Subscription-Key': xkey,  # stream 請求標頭
                  'Content-Type': 'application/octet-stream'}
xheaders_json = {'Ocp-Apim-Subscription-Key': xkey,    # json 請求標頭
                'Content-Type': 'application/json'}
xheaders = {'Ocp-Apim-Subscription-Key': xkey}         # GET 的請求標頭

img_info=suaia.subot_faceInfo(img=ximg,base=xbase,headers_stream=xheaders_stream)

###轉換成為中文資料:
img_info_gender=img_info[0]['faceAttributes']['gender']
if img_info_gender=='male':
    xGender='男生'
else:
    xGender='女生'
    
img_info_age=img_info[0]['faceAttributes']['age']

img_info_emotion=img_info[0]['faceAttributes']['emotion']
img_info_emotion=sorted(img_info_emotion.items(), key=lambda x: x[1],reverse=True)
if img_info_emotion[0][0]=='neutral':
    xEmotion='是平淡的'
elif img_info_emotion[0][0]=='contempt':
    xEmotion='有點輕蔑的'
elif img_info_emotion[0][0]=='happiness':
    xEmotion='是快樂的'
elif img_info_emotion[0][0]=='anger':
    xEmotion='有點生氣的'
elif img_info_emotion[0][0]=='disgust':
    xEmotion='有些厭惡感的'
elif img_info_emotion[0][0]=='fear':
    xEmotion='有些害怕的'
elif img_info_emotion[0][0]=='sadness':
    xEmotion='有點悲傷的'
else:
    xEmotion='有些驚訝的'

img_info_hairColor=img_info[0]['faceAttributes']['hair']['hairColor']
img_info_hairColor=sorted(img_info_hairColor, key=operator.itemgetter("confidence"),reverse=True)

faceId = img_info[0]['faceId']              # 取得 FaceId
personId=suaia.subot_faceIdentify(faceId,base=xbase,gid=xgid,headers_json=xheaders_json)   # 取得 PersonId
personsInfo=suaia.subot_personList(base=xbase,gid=xgid,headers=xheaders)
    
for p in personsInfo:       # 取得清單中 personId 的姓名資訊
    if personId == p['personId']:
        print('歡迎:', p['name'])
        print('您的性別是:',xGender)
        print('看來您的年齡大約是:',img_info_age,'歲左右')
        print('從臉部表情看來，您的情緒表情是',xEmotion)
        words_Info1='嗨'+p['name']+'，歡迎您。'
        words_Info2='從鏡頭看來，'+'您的性別是:'+str(xGender)
        words_Info3='我估計您的年齡大約是:'+str(img_info_age)+'歲左右'
        words_Info4='從臉部表情看來，您的情緒表情是'+str(xEmotion)
        suaib.subot_talks(words_Info1)
        cv2.waitKey(100)
        suaib.subot_talks(words_Info2)
        cv2.waitKey(100)
        suaib.subot_talks(words_Info3)
        cv2.waitKey(100)
        suaib.subot_talks(words_Info4)
        suaib.subot_talks('歡迎'+ p['name']+'來到課程上課')
        #sudb_addName(name= p['name'])     # 存入資料庫
        #sudb_checkDb()            
    
    



    
    
    
    
    
    
    
    
    
    
    
    
    
    