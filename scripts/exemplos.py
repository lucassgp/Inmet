# -*- coding: utf-8 -*-

driver_path = 'chromedriver.exe' # caminho completo do driver.exe

# uso do consultas_inmet_v1
import consultas_inmet_v1 as imt1

# Consultando informacoes basicas das estacoes
estacoes = imt1.consulta_estacoes_inmet(driver_path) 

# Consultando dados meteorologicos da estacao desejada 
dados = imt1.ConsultaDadosEstacao(driver_path=driver_path, # caminho completo do driver.exe
                                  cod_estacao='A726', # codigo da estacao
                                  dinicial='01/04/2022', # formato dd/mm/aaaa
                                  dfinal='01/07/2022')   # formato dd/mm/aaaa - periodo menor que 6 meses

tabela = dados.dados_brutos # tabela com os dados meteorologicos brutos 
tabela_tratada = dados.organizar_tabelas() # dicionario com as tabelas ja tratadas e separadas por categoria

#-----------------------------------------------------------------------------------------------------------------------------
# uso do consultas_inmet_v2
import consultas_inmet_v2 as imt2

estacoes, dados_geograficos = imt2.consulta_estacoes_inmet(driver_path = driver_path, # caminho completo do driver.exe
                                                           cod_ibge='3538709', # codigo ibge do municipio
                                                           raio_pesquisa=1) # raio de busca (Km)

# Consultando dados meteorologicos da estacao desejada 
dados = imt1.ConsultaDadosEstacao(driver_path=driver_path, # caminho completo do driver.exe
                                  cod_estacao='A726', 
                                  dinicial='01/04/2022', # formato dd/mm/aaaa
                                  dfinal='01/07/2022')   # formato dd/mm/aaaa - periodo menor que 6 meses

tabela = dados.dados_brutos # tabela com os dados meteorologicos brutos 
tabela_tratada = dados.organizar_tabelas() # dicionario com as tabelas ja tratadas e separadas por categoria