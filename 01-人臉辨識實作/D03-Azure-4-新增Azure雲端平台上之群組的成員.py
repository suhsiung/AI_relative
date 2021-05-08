import requests
## 填寫部分 ：   ###################################################################
groupName='group01'          ## '填入群組名稱-英文,例如: group01'    
base ='https://suface3.cognitiveservices.azure.com/face/v1.0'              ## '填入端點'   
key = '5e73a46ec71a45a0b1d09100f4447324'              ## '填入金鑰'  
####################################################################################


## 填寫部分 ：   ###################################################################
name1='蘇秉緯'   ##'新增人員姓名'  
name2='輔仁大學 會計系 '   ##'新增人員單位職稱'
####################################################################################
pson_url = f'{base}/persongroups/{groupName}/persons'   # 新增人員的請求路徑
headers_json = {'Ocp-Apim-Subscription-Key': key,                        # 請求標頭
                'Content-Type': 'application/json'}   
body = {'name': name1 ,                                         # 建立請求主體內容
        'userData': name2}         
body = str(body).encode('utf-8')                                   # 請求主體的編碼
response = requests.post(pson_url,                                # HTTP POST
                         headers=headers_json, 
                         data=body)     
if response.status_code == 200:
    print('新增人員完成: ', response.json())
else:
    print("新增失敗:", response.json())                          # 印出創建失敗原因
    
###################################################################################


