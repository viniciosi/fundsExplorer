import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

colunas = ['Codigo', 'Nome', 'Preco', 'VolumeMedio', 'DividendYield', 'PatrimonioLiq', 'P/VP', 'Cotas', 'Segmento']
dfFundos = pd.DataFrame(columns=colunas)

html = urlopen("https://www.fundsexplorer.com.br/funds")
res = BeautifulSoup(html.read(),"html5lib")
tags = res.find_all("span", {"class":"symbol"})
for tag in tags:
    html = urlopen("https://www.fundsexplorer.com.br/funds/" + tag.getText())
    res = BeautifulSoup(html.read(),"html5lib")
    Codigo = tag.getText()
    Nome = res.find_all("h2", {"class":"section-subtitle"})[0].getText()
    Preco = res.find_all("span", {"class":"price"})[0].getText()
    VolumeMedio = res.find_all("span", {"class":"indicator-value"})[0].getText()
    DividendYield = res.find_all("span", {"class":"indicator-value"})[3].getText()
    PatrimonioLiq = res.find_all("span", {"class":"indicator-value"})[4].getText()
    PVP = res.find_all("span", {"class":"indicator-value"})[7].getText()
    Cotas = res.find("span", {"class":"title"}, text="Cotas emitidas").find_all_next("span")[0].getText()
    Segmento = res.find("span", {"class":"title"}, text="Segmento").find_all_next("span")[0].getText()

    linhasFundo = [Codigo, Nome, Preco, VolumeMedio, DividendYield, PatrimonioLiq, PVP, Cotas, Segmento]

    dfFundos.loc[Codigo] = linhasFundo
    

