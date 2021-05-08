## 填寫部分 ：   ###################################################################
groupName='group01'          ## '填入群組名稱-英文,例如: group01'    
base ='https://suface3.cognitiveservices.azure.com/face/v1.0'              ## '填入端點'   
key = '5e73a46ec71a45a0b1d09100f4447324'              ## '填入金鑰'  
####################################################################################

import D_000_subot_func as suaia

## 填寫部分 ：   ###################################################################
pid1=''     ##'填寫人員 personId '  
####################################################################################
base1=base
key1=key
gid1=groupName
##1.初始化Azure平台的端點與金鑰
suaia.subot_faceInit(b=base1,k=key1)       # 初始化端點和金鋪
##2.查詢Azure平台上 群組 gp01上的成員與編號
suaia.subot_personList(gid1)
########################################################################
###
####以下針對成員 pidIn 進行資料處理:
###
pidIn=pid1               #指定要操作的 gid 和 pid
###
###
##3.找定要操作的 群組與成員
suaia.subot_faceUse(gid1, pidIn)            
##4.利用攝影機 進行拍照與上傳到Azure新增人員的人臉影像:
suaia.subot_faceShot('add')      # 呼叫拍照函式來拍照並上傳到Azuse新增成員人臉影像
#############################################################################
##5.要求Azure 開始進行訓練:
import requests
train_url = f'{base1}/persongroups/{gid1}/train' # 請求路徑
headers = {'Ocp-Apim-Subscription-Key': key1}   # 請求標頭
response = requests.post(train_url,            # POST 請求
                         headers = headers)
if response.status_code == 202:     
    print("開始訓練...")
else:
    print("訓練失敗", response.json())
#############################
##6.查看Azure 訓練進度:
training_url = f'{base1}/persongroups/{gid1}/training' # 請求路徑
response = requests.get(training_url,              # GET 請求
                        headers = headers)
if response.status_code == 200:     
    print("訓練結果：", response.json())
else:
    print("查看失敗", response.json())
##############################################################################
    
    
    
    
    