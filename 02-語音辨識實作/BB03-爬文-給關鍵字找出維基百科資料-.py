
import B_000_subot_func as suai

listenText = suai.subot_listen('zh-tw')
#listenText ="圖靈"
keyword=listenText

textWiki=suai.subot_getWiki(keyword)

print(textWiki)

suai.subot_talks(textWiki)
