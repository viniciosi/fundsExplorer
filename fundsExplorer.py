from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.fundsexplorer.com.br/funds")
res = BeautifulSoup(html.read(),"html5lib")
tags = res.find_all("span", {"class":"symbol"})
for tag in tags:
    html = urlopen("https://www.fundsexplorer.com.br/funds/" + tag.getText())
    res = BeautifulSoup(html.read(),"html5lib")
    descr = res.find_all("h2", {"class":"section-subtitle"})[0].getText()
    preco = res.find_all("span", {"class":"price"})[0].getText()
    print(descr)

