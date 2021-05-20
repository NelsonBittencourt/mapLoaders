# -*- coding: utf-8 -*-

"""
******************************************************************************
Rotinas para interpretar vários formatos de dados para utilização no 'plotMap'
              
Autor   : Nelson Rossi Bittencourt
Versão  : 0.11
Licença : MIT
Dependências: numpy, pygrib (que tem várias dependências adicionais) e re

    Para instalar o pygrib, use:

        conda install -c conda-forge pygrib

    ou 

        pip install pygrib


******************************************************************************
"""

import numpy as np
import pygrib
import re

def chuvaTxtONS(nomeArquivo, soValores=False):
    """
    Lê os dados de chuva prevista dos arquivos texto fornecidos pelo ONS.

    Argumentos
    ----------   
    nomeArquivo : nome do arquivo 'txt' no formato ONS.
        O arquivo deve formado por linhas do tipo:
        
        AAAAAA BBBBBB CCCCCC
        
        Onde:
            AAAAAA - longitude, duas casas decimais;
            BBBBBB - latitude, duas casas decimais;
            CCCCCC - valor da chuva, uma casa decimal.

    soValores : (Opcional) Flag para selecionar os vetores de retorno da função. Veja retornos abaixo.
        Útil quando diversos arquivos com a mesma disposição de coodernadas são lidos sequencialmente.

    Retornos
    --------
    Se soValores = 'False', retorna os vetores de longitudes, latitudes e chuvas;

    Se soValores = 'True', retorna o vetor de chuvas somente.
    
    """

    # Listas para acomodares os dados a serem lidos do arquivo txt do ONS.
    chuva = []
    lons = []
    lats = []
    
    # Flag parar indicar a necessidade de transpor a matriz de chuvas caso seja necessário.
    needsTranspose = False

    # Número de linha lida do arquivo txt. Essa variável será utilizada para determinar o ponto do
    # arquivo txt onde será realizada um teste para verificar se as longitudes ou as latitudes estão
    # variando primeiro.
    numLinha = 0      
    
    try:
        with open(nomeArquivo, 'r') as f:
            for line in f:                
                # As longitude e latitudes são lidas como texto e mantidas nesse formato nas listas.
                # Posteriormente, serão transformada em 'float'.
                # Obtêm um lista com 3 valores (longitude, latitude e chuva prevista).
                tmp = re.findall(r'[-+]?\d*\.\d+|\d+', line)

                # Aloca longitude e latitude na forma de string.
                lon = tmp[0]
                lat = tmp[1]

                # Aloca o valor de chuva no formato 'float'.
                chuva.append(float(tmp[2]))
                
                # Só considera as longitutes ou latitudes não repetidas.
                if (lon not in lons):
                    lons.append(lon)
                if (lat not in lats):
                    lats.append(lat)

                # Se já tiverem sido lidas 5 linhas do arquivo txt, executa o teste da 
                # necessidade de transpor os valores.
                if (numLinha == 5):
                    if (len(lats)>len(lons)):
                        needsTranspose = True   # Se o número de latitudes > número de longitudes, seta a transposição.
                
                numLinha = numLinha + 1

    except:
        raise NameError('Erro ao tentar abrir/acessar arquivo: {}'.format(nomeArquivo))       
  
    # Conversão dos valores de 'string' para 'float'
    lons = [float(i) for i in lons]
    lats = [float(i) for i in lats] 
   
    # Transforma a lista 'chuva' em uma matriz e altera o seu 'formato' para compatibilidade com a o número de longitutes 
    # e latitudes. Veja o método 'reshape' do 'numpy' para maiores detalhes.
    chuva = np.array(chuva,dtype=float)    

    # Caso seja necessário,  transpõe a matriz.
    if (needsTranspose):                  
        chuva = np.reshape(chuva,(len(lons),-1))    
        chuva = np.transpose(chuva)            
    else:
        chuva = np.reshape(chuva,(len(lats),-1))
    
    # Retorna todos os vetores ou só o vetor de chuvas.
    if (soValores):
        return chuva
    else:        
        return lons, lats, chuva


def chuvaCPTEC(nomeArquivo, numMsgGrib, multChuva):
    """
    Lê os dados de chuva prevista dos arquivos do modelo ETA do CPTEC.

    Com alguns ajustes, será possível ler outros tipos de arquivo já que utiliza o 'pygrib'
    para interpretar os valores.

    O 'pygrib' pode ser utilizado para ler arquivos tipo 'grib-1' e 'grib-2'.

    Argumentos
    ----------   
    nomeArquivo : nome do arquivo 'grib' ou 'grib2' contendo do dados de chuva do modelo ETA.

    numMsgGrib : número da mensagem do arquivo 'grib' com os dados de chuva.
        Para o modelo ETA do CPTEC, a mensagem de chuva é a 14.

    multChuva : valor numérico para multiplicar o vetor de chuva final.
        Para o modelo ETA, o multiplicador deve ser 1000.
        
    
    Retornos
    --------
    Vetor de longitudes, vetor de latitudes e matriz de precipitações.
    
    """

    # Lê todas as mensagens do arquivo 'grib-1' ou 'grib-2'.
    grbs = pygrib.open(nomeArquivo)    
        
    # Aloca os valores da mensagem de chuva na variável correspodente.
    chuva = grbs[numMsgGrib].values   
    
    # Transforma o variável 'chuva' em um matriz de 'floats'.
    chuva = np.array(chuva,dtype=float) 

    # Lê as latitudes de longitudes da mesma mensagem do arquivo grib.
    lats, lons = grbs[numMsgGrib].latlons()

    # Elimina valores desnecessários dos vetores de longitude e latitude.
    lons = lons[0]
    lats = lats[:,0]

    return lons, lats, (chuva * multChuva)

