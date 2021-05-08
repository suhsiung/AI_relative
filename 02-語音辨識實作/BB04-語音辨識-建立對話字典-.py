
import B_000_subot_func as suai

getWords = ''
getQa= ''
QA = {'你是誰' : '我是大雄', '聽不懂' : '請再說一次問題',
      '早安' : '太陽都曬到屁股，還在早安!',
      '午安' : '我們該吃午餐了，想出去買嗎？',
      '晚安' : '還早啦！我們再來喝個茶吧！'
      }
try:
    getWords=suai.subot_listen()         # 打開耳朵聽問題
    getQa=QA.get(getWords,'等我學多一點能力，再跟你回答這類問題')
except Exception:
    getWords='None...'
    getQa='請您說話'

while not getWords=='再見':
    suai.subot_talks(getQa)
    try:
        getWords=suai.subot_listen()
        getQa=QA.get(getWords,'等我學多一點能力，再跟你回答這類問題')
        xt1=4
    except Exception:
        getWords='None...'
        print('wait talks時，發生通用錯誤,等待2秒後繼續...')
        getQa='請您說話'
        xt1=1
   
suai.subot_talks('再見')

 