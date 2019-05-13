import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

colunasFundo = ['Codigo', 'Nome', 'Preco', 'VolumeMedio', 'DividendYield', 'PatrimonioLiq', 'P/VP', 'Cotas', 'Segmento']
dfFundos = pd.DataFrame(columns=colunasFundo)

colunasAtivo = ['codigo', 'titulo', 'endereco', 'bairro', 'estado', 'cidade', 'area']
dfAtivos = pd.DataFrame(columns=colunasAtivo)

html = urlopen("https://www.fundsexplorer.com.br/funds")
res = BeautifulSoup(html.read(),"html5lib")
tags = res.find_all("span", {"class":"symbol"})
for tag in tags:
    html = urlopen("https://www.fundsexplorer.com.br/funds/" + tag.getText())
    res = BeautifulSoup(html.read(),"html5lib")
    Codigo = tag.getText()
    Nome = res.find_all("h2", {"class":"section-subtitle"})[0].getText()
    Preco = res.find_all("span", {"class":"price"})[0].getText().split("\n")[1].strip()
    VolumeMedio = res.find_all("span", {"class":"indicator-value"})[0].getText().split("\n")[1].strip()
    DividendYield = res.find_all("span", {"class":"indicator-value"})[3].getText().split("\n")[1].strip()
    PatrimonioLiq = res.find_all("span", {"class":"indicator-value"})[4].getText().split("\n")[1].strip()
    PVP = res.find_all("span", {"class":"indicator-value"})[7].getText().split("\n")[1].strip()
    Cotas = res.find("span", {"class":"title"}, text="Cotas emitidas").find_all_next("span")[0].getText().split("\n")[1].strip()
    Segmento = res.find("span", {"class":"title"}, text="Segmento").find_all_next("span")[0].getText().split("\n")[1].strip()

    linhasFundo = [Codigo, Nome, Preco, VolumeMedio, DividendYield, PatrimonioLiq, PVP, Cotas, Segmento]

    dfFundos.loc[Codigo] = linhasFundo

    ativos = res.find("div", {"id":"fund-actives-items"})
    if ativos:
        for ativo in ativos.find_all("div", {"class":"items-wrapper"}):
            titulo = ativo.find("span", {"title"}).getText()
            endereco = ativo.find_all("li")[0].getText().split(":")[1].strip()
            bairro = ativo.find_all("li")[1].getText().split(":")[1].strip()
            estado = ativo.find_all("li")[2].getText().split(":")[1].strip().split(" - ")[1]
            cidade = ativo.find_all("li")[2].getText().split(":")[1].strip().split(" - ")[0]
            area = ativo.find_all("li")[3].getText().split(":")[1].strip()

            linhasAtivos = [Codigo, titulo, endereco, bairro, estado, cidade, area]

            dfAtivo = pd.DataFrame(columns=colunasAtivo)
            dfAtivo.loc[Codigo] = linhasAtivos
            dfAtivos = dfAtivos.append([dfAtivo])

indNA = dfFundos["VolumeMedio"] != 'N/A'
indZero = dfFundos["VolumeMedio"] != '0'

dfFundos = dfFundos[indNA]
dfFundos = dfFundos[indZero]

dfAtivos = dfAtivos[indNA]
dfAtivos = dfAtivos[indZero]

dfFundos.to_csv("fundos.csv", sep = ";", encoding = 'utf-8-sig')

dfAtivos.to_csv("ativos.csv", sep = ";", encoding = 'utf-8-sig')

dfFundos['Segmento'].describe()
dfFundos['Segmento'].unique()

dfFundos.describe()

dfAtivos.describe()

dfAtivos.estado.value_counts()