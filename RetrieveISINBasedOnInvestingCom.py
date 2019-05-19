import requests
import re
import time

def getisinfrompage(pageurl):
    
    

    result = session_requests.get(
    url = pageurl, 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'},
    ) 
    
    return re.findall(r'<title>.+? \| (.+?) Stock Price - Investing.com</title>', result.text)[0] + ' , ' +re.findall(r'ISIN:</span>\n                <span class="elp" title="(.+?)&nbsp;" >.+</span>', result.text)[0]
    
def getisinfromindex(originurl):

    url = originurl+'-components'
    
    result = session_requests.get(
        url = url, 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'},
    )
    print (result)
    
    remining = re.findall(r'>Download Data</a>(.+?)</table>', str(result.content))[0]
    items = re.findall(r'<a href="/equities/.+?</a>', remining)

    for item in items:

        company = re.findall(r'<a href="(/equities/.+)"  t', item)[0]
        purl = 'https://www.investing.com'+company
        print (getisinfrompage(purl))
        time.sleep(5)
 
 # Example:
 session_requests = requests.session()
 getisinfromindex('https://www.investing.com/indices/idx-30')
