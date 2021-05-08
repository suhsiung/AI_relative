
import B_000_subot_func as suai
        
sen1='我要學會使用人工智慧的語音辨識，現在正使用Google的語音辨識功能讓電腦說話!'  
suai.subot_talks(sen1)

## 文字轉語音:
textData1="致理科技大學，商務管理學院，大數據實驗室"
suai.subot_talks(textData1)

textData2="Ladies and gentlemen,now the topic i am going to present to you is AI and\
            big data."
suai.subot_talks(textData2,'en')

textData3="紳士淑女、今私があなたに提示しようとしているトピックはAIと\です。ビッグデータ。"
suai.subot_talks(textData3,'ja')