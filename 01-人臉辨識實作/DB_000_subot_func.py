
import speech_recognition as spee # 匯入套件並命名為 spee
import os
from gtts import gTTS
from pygame import mixer
import tempfile
from bs4 import BeautifulSoup
import requests
import re
from hanziconv import HanziConv

mixer.init()
if not os.path.isfile('init0.mp3'):    # 不重要的聲音檔產生器
    tts = gTTS(text = '初始化的語音檔', lang = 'zh-tw')
    tts.save('init0.mp3')
    print('已產生初始化的語音檔 init0.mp3')
#-----------------#


def subot_listen(country='zh-TW'):
    listen1 = spee.Recognizer()                  # 產生語音辨識物件
    with spee.Microphone() as source:            # 使用麥克風取得語音
        listenData = listen1.listen(source)      # 產生語音資料物件
    try:
        listenWords = listen1.recognize_google(listenData, language=country)     
                                                 # 將語音資料轉換為文字資料(繁體中文)
        return listenWords
    except:
        return '我聽不清楚...! I can not hear clearly!'

def subot_talks(contents,country='zh-TW'):
    try:
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts=gTTS(text=contents,lang=country) #zh-TW 中文
            ##  英文是 en, 日文是 ja, 法文是 fr, 俄語是 ru, 西班牙語是 es, 任何語言都可以
            ##  https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
            tts.save("{}.mp3".format(fp.name))
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play()
            while(mixer.music.get_busy()):
                continue
    except:
        print('播放文字語音失敗....')
        
##爬文 維基百科 +關鍵字 搜尋後相關資料: subot_gotWiki('關鍵字')
def subot_getWiki(keyword):
    response = requests.get('https://zh.wikipedia.org/zh-tw/' + keyword)
    bs = BeautifulSoup(response.text, 'lxml')
    p_list = bs.find_all('p')
    for p in p_list:
        if keyword in p.text[0:10]:
            return p.text     

## 先清理sentence內容後，並將中文、英文分開後再透過電腦轉成語音: subot_talks_re(文字內容)
def subot_talks_re(sentence):
	s1 = re.sub(r'\[[^\]]*\]', '', sentence)
	print(s1)
	en_list = re.findall(r'[a-zA-Z ]+',s1)
	s2 = re.sub(r'[a-zA-Z \-]+', '@English@', s1)
	all_list = s2.split('@')
	index = 0
	for text in all_list:
		if text != 'English':    
			subot_talks(text, 'zh-tw')
		else:
			subot_talks(en_list[index], 'en')
			index += 1

## 將複雜的問題轉換成關鍵字: subot_getGoogle(問題文字)
def subot_getGoogle(question):
    url = f'https://www.google.com.tw/search?q={question}+維基百科'
    response = requests.get(url)
    if response.status_code == 200:    
        bs = BeautifulSoup(response.text, 'lxml')
        wiki_url = bs.find('cite')
        kwd = wiki_url.text.split('/')[-1]
        keyword_trad = HanziConv.toTraditional(kwd)
        return keyword_trad
    else:
        print('解讀後轉換關鍵字失敗....')









