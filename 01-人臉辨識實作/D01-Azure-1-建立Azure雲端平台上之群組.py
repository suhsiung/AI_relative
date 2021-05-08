
import requests

## 填寫部分 ：   ###################################################################

groupName='group01'          ## '填入群組名稱-英文,例如: group01'    
base ='/face/v1.0'              ## '填入端點'   
key = ''              ## '填入金鑰'  
####################################################################################

gp_url = base + '/persongroups/' + groupName            # 創建群組的請求路徑
headers_json = {'Ocp-Apim-Subscription-Key': key,       # 請求標頭
                'Content-Type': 'application/json'}  
 
body = {'name': groupName ,            ## 建立請求主體內容: name最多128
        'userData': '創建群組'}         ## userData最多16KB
body = str(body).encode('utf-8')          # 請求主體的編碼

response = requests.put(gp_url,         # HTTP PUT 
                        headers = headers_json, 
                        data = body)            
if response.status_code == 200:                # 請求成功返回狀態碼 200
    print("創建群組成功")    
else:
    print("創建失敗:", response.json())         # 印出創建失敗原因

##ref: https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395244
    