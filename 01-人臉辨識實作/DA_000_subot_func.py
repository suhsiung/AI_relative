
##需要導入的套件
import cv2,requests
import time
from datetime import datetime
import sqlite3
import DB_000_subot_func as suaib


def subot_faceInit(b, k):
    global base, key, headers_stream, headers_json, headers
    base = b   # 端點
    key = k
    headers_stream = {'Ocp-Apim-Subscription-Key': key,  # stream 請求標頭
                      'Content-Type': 'application/octet-stream'}
    headers_json = {'Ocp-Apim-Subscription-Key': key,    # json 請求標頭
                    'Content-Type': 'application/json'}
    headers = {'Ocp-Apim-Subscription-Key': key}         # GET 的請求標頭

def subot_faceUse(g, p):
    global gid, pid
    gid = g
    pid = p

def subot_personList(base,gid,headers):
    pson_url = base + f'/persongroups/{gid}/persons'    # 查看群組人員的請求路徑
    response = requests.get(pson_url,          # HTTP GET
                            headers=headers)     
    if response.status_code == 200:
        print('查詢人員完成')
        return response.json()
    else:
        print("查詢人員失敗:", response.json())         # 印出創建失敗原因

def subot_faceAdd(img):                        # 建立自訂函式
    img_encode = cv2.imencode('.jpg', img)[1]       # 將 img 編碼為 jpg 格式，[1]返回資料, [0]返回是否成功
    img_bytes = img_encode.tobytes()                # 再將資料轉為 bytes, 此即為要傳送的資料
    face_url = f'{base}/persongroups/{gid}/persons/{pid}/persistedFaces'       # 新增臉部資料的請求路徑
    response = requests.post(face_url,              # POST 請求
                         headers= headers_stream,
                         data=img_bytes)
    if response.status_code == 200:
        print('新增臉部成功: ', response.json())
    else:
        print('新增臉部失敗: ', response.s)

def subot_faceDetect(img):
    detect_url = f'{base}/detect?returnFaceId=true' # 臉部偵測的請求路徑
    img_encode = cv2.imencode('.jpg', img)[1]       # 將 img 編碼為 jpg 格式，[1]返回資料, [0]返回是否成功
    img_bytes = img_encode.tobytes()                # 再將資料轉為 bytes, 此即為要傳送的資料
    response = requests.post(detect_url,
                             headers=headers_stream,
                             data=img_bytes)
    if response.status_code == 200:
        face = response.json()
        if not face:
            print("照片中沒有偵測到人臉")
        else:
            faceId = face[0]['faceId']              # 取得 FaceId
            return faceId

def subot_faceInfo(img,base,headers_stream):
    detect_url = f'{base}/detect?returnFaceId=true &returnFaceAttributes=age,gender,smile,hair,emotion'
    # headPose, smile, facialHair, glasses, emotion, hair, makeup, occlusion,
    # accessories, blur, exposure, noise' # 臉部偵測的請求路徑
    img_encode = cv2.imencode('.jpg', img)[1]       # 將 img 編碼為 jpg 格式，[1]返回資料, [0]返回是否成功
    img_bytes = img_encode.tobytes()                # 再將資料轉為 bytes, 此即為要傳送的資料
    response = requests.post(detect_url,
                             headers=headers_stream,
                             data=img_bytes)
    if response.status_code == 200:
        face = response.json()
        if not face:
            print("照片中沒有偵測到人臉")
        else:
            #faceId = face[0]['faceId']              # 取得 FaceId
            return face
    else:
        print("Azure detect 失敗",response.status_code)


def subot_faceIdentify(faceId,base,gid,headers_json):
    idy_url = f'{base}/identify'                    # 臉部偵測的請求路徑
    body = str({'personGroupId': gid,
    			'faceIds': [faceId]})
    response = requests.post(idy_url,       # 臉部驗證請求 POST
                             headers=headers_json,
                             data=body)
    if response.status_code == 200:
        person = response.json()
        if not person[0]['candidates'] :
            return None
        else:
            personId = person[0]['candidates'][0]['personId']   # 取得 personId
            print(personId)
            return personId

def sudb_addName(name,db='mydatabase.sqlite'):
    path='./A0-setup/'
    connect = sqlite3.connect(path+db)    # 與資料庫連線
    # 新建 mytable 資料表  (如果尚未建立的話)
    sql = 'CREATE TABLE IF NOT EXISTS mytable \
            ("姓名" TEXT, "打卡時間" TEXT)'
    connect.execute(sql)     # 執行 SQL 語法
    # 取得現在時間
    save_time = str(datetime.now().strftime('%Y-%m-%d %H.%M.%S'))
    # 新增一筆資料的 SQL 語法
    sql = f'insert into mytable values("{name}", "{save_time}")'
    connect.execute(sql)         # 執行 SQL 語法
    connect.commit()             # 更新資料庫
    connect.close()              # 關閉資料庫
    print('儲存成功')
    #------------------------------#        
        
def sudb_checkDb(db='mydatabase.sqlite'):
    try:
        path='./A0-setup/'
        connect = sqlite3.connect(path+db)   # 與資料庫連線
        sql = 'select * from mytable'   # 選取資料表中所有資料的 SQL 語法
        cursor = connect.execute(sql)   # 執行 SQL 語法得到 cursor 物件
        dataset = cursor.fetchall()     # 取得所有資料
        print('姓名\t打卡時間')
        print('----\t  ----')
        for data in dataset:
        	print(f"{data[0]}\t{data[1]}")
    except:
        print('讀取資料庫錯誤')
    connect.close()
    #---------------------------#  


def subot_faceWho(img):
    faceId = subot_faceDetect(img)   # 執行臉部偵測, 取得 faceId
    personId = subot_faceIdentify(faceId) # 用 faceId 進行臉部辨識, 找出群組中最像的人, 取得 personId
    if personId == None:
        print('查無相符身分')
        suaib.subot_talks('查無相符身分')
    else:
        persons = subot_personList(gid)     # 取得群組的成員清單
        for p in persons:       # 取得清單中 personId 的姓名資訊
            if personId == p['personId']:
                print('歡迎:', p['name'])
                suaib.subot_talks('歡迎'+ p['name']+'來到通識課程上課')
                sudb_addName(name= p['name'])     # 存入資料庫
                sudb_checkDb()                    # 查看資料庫


## 利用攝影機 鎖定一個人來 倒數5秒拍照 : subot_faceShot()
def subot_faceShot(function='who',num=0):
    isCnt = False       # 用來判斷是否正在進行倒數計時中
    face_detector = cv2.CascadeClassifier('./A0-setup/haarcascade_frontalface_default.xml')  # 建立臉部辨識物件
    capture = cv2.VideoCapture(num)                   # 開啟編號 0 的攝影機
    while capture.isOpened():                      # 判斷攝影機是否開啟成功
        sucess, img = capture.read()            # 讀取攝影機影像
        if not sucess:
            print('讀取影像失敗')
            continue
        img_copy = img.copy()                       # 複製影像
        faces = face_detector.detectMultiScale(     # 從攝影機影像中偵測人臉
                    img,
                    scaleFactor=1.1,
                    minNeighbors=3,
                    minSize=(50,50))
        if len(faces) == 1:                     # 如果偵測到一張人臉
            if isCnt == False:
                t1 = time.time()                # 紀錄現在的時間
                isCnt = True                    # 告訴程式目前進入倒數狀態
            cnter = 3 - int(time.time() - t1)   # 更新倒數計時器
            for (x, y, w, h) in faces:          # 畫出人臉位置
                cv2.rectangle(                  # 繪製矩形
                        img_copy, (x, y), (x+w, y+h),
                        (0, 255, 255), 2)
                cv2.rectangle(                  # 繪製矩形
                        img_copy, (x+int(w/4), y+2), (x+int(w/4)+150, y-40),
                        (255,0, 0), -1)
                cv2.putText(                    # 繪製倒數數字
                        img_copy, str(cnter)+' second',
                        (x+int(w/4), y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2)
            if cnter == 0:                  # 倒數結束
                isCnt = False               # 告訴程式離開倒數狀態
                path='./A0-output/'
                filename = datetime.now().strftime(
                        '%Y-%m-%d %H.%M.%S')        # 時間格式化
                cv2.imwrite(path+filename + '.jpg', img) # 儲存影像檔案
                #-----------------------------------------#
                if function == 'add':         # 打卡系統新增人員
                    subot_faceAdd(img)
                elif function == 'who':  # 進行人臉身分識別功能
                    subot_faceWho(img)
                else:
                    xxface=subot_faceInfo(img)
                    print(xxface)
                #-----------------------------------------#
        else:                                 # 如果不是一張人臉
            isCnt = False                     # 設定非倒數狀態

        cv2.imshow('Frame', img_copy)         # 顯示影像
        k = cv2.waitKey(1)                    # 讀取按鍵輸入(若無會傳回 -1)
        if k == ord('q') or k == ord('Q'):  # 按下 q 離開迴圈, 結束程式
            print('exit')
            cv2.destroyAllWindows()           # 關閉視窗
            capture.release()                 # 關閉攝影機
            break                             # 離開無窮迴圈, 結束程式
    else:
        print('開啟攝影機失敗')
#-----------------------------------#
        
def subot_faceShot2(num=0):
    face_detector = cv2.CascadeClassifier('./lib/haarcascade_frontalface_default.xml')  # 建立臉部辨識物件
    capture = cv2.VideoCapture(num)                   # 開啟編號 0 的攝影機
    while capture.isOpened():                      # 判斷攝影機是否開啟成功
        sucess, img = capture.read()            # 讀取攝影機影像
        if not sucess:
            print('讀取影像失敗')
            continue
        img_copy = img.copy()                       # 複製影像
        faces = face_detector.detectMultiScale(     # 從攝影機影像中偵測人臉
                    img,
                    scaleFactor=1.1,
                    minNeighbors=3,
                    minSize=(50,50))
        if len(faces) == 1:                     # 如果偵測到一張人臉
            for (x, y, w, h) in faces:          # 畫出人臉位置
                cv2.rectangle(                  # 繪製矩形
                        img_copy, (x, y), (x+w, y+h),
                        (0, 255, 255), 2)
                cv2.rectangle(                  # 繪製矩形
                        img_copy, (x+int(w/4), y+2), (x+int(w/4)+150, y-40),
                        (255,0, 0), -1)
            cv2.rectangle(                  # 繪製矩形
                    img_copy, (x+int(w/40), y+2), (x+int(w/40)+350, y-40),
                    (255,0, 0), -1)
            cv2.putText(                    # 繪製倒數數字
                    img_copy, 'Watch Here! Press Q key!',
                    (x+int(w/20), y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 1)
        cv2.imshow('Frame', img_copy)         # 顯示影像
        k = cv2.waitKey(1)                    # 讀取按鍵輸入(若無會傳回 -1)
        if k == ord('q') or k == ord('Q'):  # 按下 q 離開迴圈, 結束程式
            print('進行辨識中....')
            cv2.destroyAllWindows()           # 關閉視窗
            capture.release()                 # 關閉攝影機
            break                            # 離開無窮迴圈
    else:
        print('開啟攝影機失敗')
    return img
#--------------------------------------------------------------------------------#    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        