#import requests
#from bs4 import BeautifulSoup
#url = 'https://www.gismeteo.ru/diary/4618/2023/9/'
#html_text=requests.get(url).text
#soup=BeautifulSoup(html_text,'lxml')
#title=soup.title
#print(title)

import os 
from bs4 import BeautifulSoup 
import requests 
 
URL = "https://www.gismeteo.ru/diary/4618/2023/9/" 
html_page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}) 
soup=BeautifulSoup(html_page,'lxml') 
title=soup.title 
print(title)