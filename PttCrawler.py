# coding=UTF-8

import time
from datetime import datetime
import requests
import time
import sys
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


PttName=''
payload={
'from':'/bbs/'+PttName+'/index.html',
'yes':'yes' 
}

def getPageNumber(content) :
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex+5 : endIndex]
    return pageNumber

# pyhton PttCrawler.py AKB48 2 
if __name__ == "__main__":
    
    #PttName = raw_input('請輸入版名：')
    PttName = str(sys.argv[1])
    ParsingPage = int(sys.argv[2])
    print 'Start parsing [',PttName,']....'
    start_time = time.time()
    rs=requests.session()
    res=rs.post('https://www.ptt.cc/ask/over18',verify=False,data=payload)
    res=rs.get('https://www.ptt.cc/bbs/'+PttName+'/index.html',verify=False)
    soup=BeautifulSoup(res.text,'html.parser')
    ALLpageURL = soup.select('.btn.wide')[1]['href']
    ALLpage=int(getPageNumber(ALLpageURL))+1
    print 'Total pages:',ALLpage
    obj=[]
    URLlist=[]
    FILENAME='PttData-'+PttName+'-'+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.txt'
    file = open(FILENAME, 'a')  

    for number in range(ALLpage, ALLpage-int(ParsingPage),-1):
        url = 'https://www.ptt.cc/bbs/'+PttName+'/index'+str(number)+'.html'
        #print 'page:',number
        res=rs.get(url,verify=False)
        soup=BeautifulSoup(res.text,'html.parser')
        UrlPer=[]
        for entry in soup.select('.r-ent'):
            atag=entry.select('.title')[0].find('a') 
	    if(atag!=None):
               URL=atag['href']   
               #print 'URL:',URL          
               UrlPer.append('https://www.ptt.cc'+URL)   
                     
        for listURL in reversed(UrlPer):
            URLlist.append(listURL)
            #print 'url:',listURL
    
    
    strNext=u"\n\n\n\n***************下一篇***************\n\n\n\n\n";
    for URL in URLlist:
        res=rs.get(URL,verify=False)
        soup=BeautifulSoup(res.text,'html.parser')
        content=soup.select('.bbs-screen.bbs-content')[0].text
        obj.append(content+strNext)
        time.sleep(0.05) 
    
    
    line=''
    for data in obj:          
        line+=data
    file.write(line.encode('utf8'))
    file.close()
      
    print '====================END===================='
    print 'execution time:' + str(time.time() - start_time)+'s'
    
