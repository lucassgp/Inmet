# -*- coding: utf-8 -*-

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings("ignore")

#%%

def consulta_estacoes_inmet(driver_path = str):
    '''
    Funcao para consultar informacoes basicas das estacoes

    Parameters
    ----------
    estacao : str
        DESCRIPTION. tipo da estacao: a/c
    driver_path : str
        DESCRIPTION. Local do driver do google chrome (local para download: https://chromedriver.chromium.org/downloads)

    Returns
    -------
    estacoes : DataFrame
        DESCRIPTION. DataFrame com informacoes das etacoes do INMET
    '''

    folder_chrome_driver=driver_path # necesario um driver do navegador
    chrome_options = Options()
    chrome_options.headless = True # opcao para esconder o navegador, durante o processo
    navegador = webdriver.Chrome(options=chrome_options,executable_path=folder_chrome_driver)

    print('Buscando estacoes automaticas...', end='')
    navegador.get('https://portal.inmet.gov.br/paginas/catalogoaut') # acessa o site das estacoes
    time.sleep(2)
    page_source = navegador.page_source
    soup = BeautifulSoup(page_source, 'lxml') 
    table = soup.find('table') # filtra a tabela
    df = pd.read_html(str(table),decimal=',', thousands='.')[0] # passa a tabela para a pandas
    estacoes = pd.DataFrame(df.to_records()) # passa a tabela para DataFrame
    print('OK')
    return estacoes

#%%
class ConsultaDadosEstacao():
    '''
    Consultar dados das estacoes
    Parameters:
    driver_path : str
        DESCRIPTION. path chromedriver.exe
    cod_estacao : str
        DESCRIPTION. Codigo da estacao automatica
    dinicial : str
        DESCRIPTION. Data inicial do periodo desejado
    dfinal : str
        DESCRIPTION. Data final do periodo desejado
    '''
    def __init__(self, driver_path=str, cod_estacao=str, dinicial=str, dfinal=str):
        folder_chrome_driver=driver_path # necesario um driver do navegador
        chrome_options = Options()
        chrome_options.headless = True # opcao para esconder o navegador, durante o processo
        navegador = webdriver.Chrome(options=chrome_options,executable_path=folder_chrome_driver)
        print('Consultando INMET...', end='')
        navegador.get(f'https://tempo.inmet.gov.br/TabelaEstacoes/{cod_estacao}') # acessa o site das estacoes
        time.sleep(3) #Recomendado para evitar ban do servidor
        navegador.find_element_by_xpath('//*[@id="root"]/div[1]/div[1]').click() # abre a aba lateral
        time.sleep(1)
        navegador.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div[4]/input').send_keys(dinicial) # adiciona a data inicial do periodo
        time.sleep(1)
        navegador.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div[5]/input').send_keys(dfinal) # adiciona a data final do periodo
        time.sleep(1)
        navegador.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[2]/button').click() # gera a tabela
        time.sleep(10) # aguarda 10 segundos para a geracao da tabela
        page_source = navegador.page_source
        soup = BeautifulSoup(page_source, 'lxml') 
        table = soup.find('table') # filtra a tabela
        df = pd.read_html(str(table),decimal=',', thousands='.')[0] # passa a tabela para a pandas
        self.dados_brutos = pd.DataFrame(df.to_records()) # passa a tabela para DataFrame
        print('OK')
        
    def organizar_tabelas(self):
        list_dfs = {}
        df=self.dados_brutos.copy()
        df.columns = ['index', 'Data', 'Hora', 'Temperatura Inst (°C)','Temperatura Máx (°C)','Temperatura Mín.(°C)',
                      'Umidade Inst.(%)', 'Umidade Máx.(%)', 'Umidade Mín.(%)',
                      'Pto. Orvalho Inst.(°C)', 'Pto. Orvalho Máx.(°C)', 'Pto. Orvalho Mín.(°C)',
                      'Pressão Inst.(hPa)', 'Pressão Máx.(hPa)', 'Pressão Mín.(hPa)',
                      'Vento Vel. (m/s)', 'Vento Dir.(°)', 'Vento Raj. (m/s)', 'Radiação Kj/m²', 'Chuva (mm)']
        
        list_dfs['temperatura']  = df[['Data', 'Hora', 'Temperatura Inst (°C)','Temperatura Máx (°C)','Temperatura Mín.(°C)']]
        list_dfs['umidade']      = df[['Data', 'Hora', 'Umidade Inst.(%)', 'Umidade Máx.(%)', 'Umidade Mín.(%)']]
        list_dfs['pto_orvalho']  = df[['Data', 'Hora', 'Pto. Orvalho Inst.(°C)', 'Pto. Orvalho Máx.(°C)', 'Pto. Orvalho Mín.(°C)']]
        list_dfs['pressao']      = df[['Data', 'Hora', 'Pressão Inst.(hPa)', 'Pressão Máx.(hPa)', 'Pressão Mín.(hPa)']]
        list_dfs['vento']        = df[['Data', 'Hora', 'Vento Vel. (m/s)', 'Vento Dir.(°)', 'Vento Raj. (m/s)']]
        list_dfs['radiacao']     = df[['Data', 'Hora', 'Radiação Kj/m²']]
        list_dfs['precipitacao'] = df[['Data', 'Hora', 'Chuva (mm)']]
        return list_dfs
