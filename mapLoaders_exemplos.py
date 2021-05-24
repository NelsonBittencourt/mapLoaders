# -*- coding: utf-8 -*-

"""
******************************************************************************
Rotinas de exemplo do uso do módulo 'mapLoaders'
              
Autor   : Nelson Rossi Bittencourt
Versão  : 0.111
Licença : MIT
Dependências: plotMap, mapLoaders
******************************************************************************
"""

import plotMap
import mapLoaders

def exemploTxtsONS():
    """
    Lê arquivos texto com chuvas previstas pelos modelos ETA40, GEFS50 e ECMWF e plota
    os mapas correspondentes.

    Os arquivos foram elaborados e fornecidos pelo ONS. Os nomes dos arquivos foram alterados
    para evitar a criação de rotinas de tratamento para os nomes originais. Essa alteração visa
    manter o código mais simples e focado no exemplo.

    Argumentos
    ----------
    nenhum

    Retornos
    --------
    nenhum
    
    """

    # Diretórios de entrada/saída dos dados.
    dirEntrada = 'txtsONS/Entrada'
    dirSaida = 'txtsONS/Saida'
   
    # Listas com os nomes dos modelos e o número de dias de previsão de cada um deles.
    nomesModelos = ['ETA40', 'GEFS', 'ECMWF']    
    diasModelos = [10,14,14]

    # Lê modelo de mapa do arquivo.
    mapaModelo = plotMap.loadMapTemplate('template/ChuvaPrevistaONS.dat')

    # Loop para os três modelos que o ONS utiliza.
    for i in range(len(nomesModelos)):

        nomeModelo = nomesModelos[i]
        numDias = diasModelos[i]

        # Lista que conterá o acumulado de chuva para o número de dias de cada modelo.
        chuvaTotal = 0

        # Loop para o número de dias de cada modelo.
        for dia in range(1,numDias+1):

            # Caminho completo para o arquivo de cada dia.
            fileName = '{0}/{1}/{1}_{2}.dat'.format(dirEntrada,nomeModelo, dia)
            
            # Se for o primeiro dia, lê as longitudes e latitudes.
            # Caso contrário, lê apenas as chuvas previstas.
            if (dia ==1):
                lons, lats, chuva = mapLoaders.chuvaTxtONS(nomeArquivo=fileName)
            else:
                chuva = mapLoaders.chuvaTxtONS(nomeArquivo=fileName,soValores=True)

            # Incrementa o vetor de chuva total com a chuva do dia.
            chuvaTotal = chuvaTotal + chuva

            # Plota o mapa diário.
            plotMap.plotarMapa(
                                titulo='Modelo {} - TXT ONS\nDia {}'.format(nomeModelo,dia),
                                lons=lons,
                                lats=lats,
                                dados=chuva,
                                modeloMapa=mapaModelo,
                                destino='{}/{}_fig_dia_{}.jpg'.format(dirSaida, nomeModelo,dia)
                                )

        # Plota o mapa com a soma de todos os dias.
        plotMap.plotarMapa(
                            titulo='Modelo {} - TXT ONS\nSoma dos {} dias'.format(nomeModelo,numDias),
                            lons=lons,
                            lats=lats,
                            dados=chuvaTotal,
                            modeloMapa=mapaModelo,
                            destino='txtsONS/Saida/{}_fig_total.jpg'.format(nomeModelo)
                            )


def exemploCPTEC(modelo):
    """
    Lê arquivos tipo 'grib' (versão 1 ou 2) com precipitações previstas através dos modelos ETA e WRF.    
    Estes arquivos são disponibilizados pelo CPTEC em sua área FTP.


    Argumento
    ---------

    modelo : pode ser 'ETA' ou ' WRF'.


    Retorno
    -------
    
    Nenhum.

    """

    # TODO: Passar as datas e horas como argumento da função.
    # Data e hora. Estes valores estão fixos no exemplo.    
    hora = 0            # Hora inicial 
    dia0 = 19           # Dia da rodada
    dia =  20           # Dia inicial da previsão
    ano = '2021'        # Ano 
    mes = '05'          # Mês

    # TODO: Passar o flag com argumento da função.
    # Flag para determina se serão plotados os mapas horários (True) ou não (False).
    flagPlotaDiario = True


    # Determina os parâmetros de cada modelo.
    # Importante: 
    # 1) ainda não confirmei os valores da variável 'multiplicador' para cada modelo;
    # 2) o número da mensagem para as precipitações previstas nos arquivos grib (numMsgGrib)
    # foi adotado como 14 para o modelo ETA e 1 para o modelo WRF. No caso do WRF, foram utilizados
    # os arquivos de 'cortes' da pasta 'prec' do FTP do CPTEC. Essa escolha foi baseada no tamanho dos 
    # arquivos. Se você escolher os arquivos 'brutos' do WRF, a mensagem será outra.
    if (modelo=='ETA'):
        filePrefix = 'eta_40km'
        filePosfix = 'grb'
        dateSeparator = '+'
        multiplicador = 1000
        numMsgGrib = 14
    elif (modelo=='WRF'):
        filePrefix='wrf_cpt_05KM'
        filePosfix = 'grib2'
        dateSeparator = '_'
        multiplicador = 1/24
        numMsgGrib = 1
    else:
        raise NameError("Para utilizar essa função é necessário fornecer o nome do modelo como argumento.")


    # Diretórios de entrada e saída.
    dirEntrada = '{0}/Entrada'.format(modelo)
    dirSAida = '{0}/Saida'.format(modelo)

    # TODO: Passar o template de mapa com argumento da função.
    # Cria um objeto 'Mapa', com o modelo de mapa, para uso no plotMap.
    mapaModelo = plotMap.loadMapTemplate('template/ChuvaPrevistaONS.dat')

    # Variável que conterá o somatório das chuvas diárias.
    chuvaTotal =  0      

    # String para a data da rodada.
    sDataRodada = ano + mes + f'{dia0:02d}' + '00'

    # String para conter a parte fixa do caminho dos arquivo a serem lidos.
    fileNameFixo = '{}/{}_{}'.format(dirEntrada, filePrefix, sDataRodada)

    # Loop para o número de períodos. Neste exemplo 24 períodos.
    for i in range(24):                                                       
        
        sHora = f'{hora:02d}'                           # String com a hora formatada.
        sDia = f'{dia:02d}'                             # String com o dia formatado.
        sDataPrevisao = ano + mes + sDia + sHora        # String com a data da previsão

        # Criar uma string com caminho completo do arquivo a ser lido.        
        fileName = '{}{}{}.{}'.format(fileNameFixo, dateSeparator, sDataPrevisao, filePosfix)

        hora = hora + 1                 # Incrementa a hora.

        # Caso o contador de horas atinja 24, reinicia o contador de horas e incrementa o contador a variável 'dia'.
        if (hora == 24):
            hora = 0
            dia = dia + 1

        # Obtem os valores do arquivo 'grib' do ETA.
        #lons, lats, chuva = mapLoaders.chuvaEtaCPTEC(fileName,14,1000)
        
        # Lê as coordenadas e a chuva prevista de cada arquivo. 
        # Preste antenção às variáveis 'numMsgGrib' e 'multiplicador'.
        lons, lats, chuva = mapLoaders.chuvaCPTEC(fileName,numMsgGrib,multiplicador)
        
        # Acumulador de chuva.
        chuvaTotal = chuvaTotal + chuva

        # Plota mapa para cada período (caso flagPlotaDiario = True).
        if (flagPlotaDiario):
            plotMap.plotarMapa(
                               titulo='Modelo {} - CPTEC Grib\nDia {}; Hora {}'.format(modelo, sDia,sHora),
                               lons=lons,
                               lats=lats,
                               dados=chuva,
                               modeloMapa=mapaModelo,
                               #destino='eta40_CPTEC/ETA_CPTEC_grib_{}{}'.format(sDia,sHora) + '.jpg'
                               destino='{}/{}_Diario_{}_{}.jpg'.format(dirSAida,filePrefix, sDia, sHora)
                               )

    # Plota mapa com valor acumulado.
    plotMap.plotarMapa(                        
                        titulo='Modelo {} - CPTEC Grib\nSomatório das Horas'.format(modelo),
                        lons=lons,
                        lats=lats,
                        dados=chuvaTotal,
                        modeloMapa=mapaModelo,
                        #destino='eta40_CPTEC/Saida/ETA_CPTEC_grib_Total.jpg'
                        destino='{}/{}_Total.jpg'.format(dirSAida,modelo)
                        )

def exemploSateliteONS():
    """
    Plota em um mapa os dados de chuva verificada por satélite.

    Importante: a rotina utilizada para ler este tipo dados deve ser utilizada com um modelo
    de mapa do tipo 'xy'. Veja o método 'mapLoaders.chuvaSateliteONS' para mais informações. 
    
    Argumentos
    ----------
    Nenhum.

    
    Retornos
    --------
    Nenhum.
        
    """

    # Carrega o template já considerando a tipo de mapa como 'xy'.
    mapaModelo = plotMap.loadMapTemplate('template/ChuvaSatONS.dat')

    # Lê os dados do arquivo.
    lons, lats, chuva = mapLoaders.chuvaSateliteONS('precSatONS/psat_23052021.txt')
    
    # Plota o mapa.
    plotMap.plotarMapa(
                       titulo='Chuva por Satélite ONS',
                       lons=lons,
                       lats=lats,
                       dados=chuva,
                       modeloMapa=mapaModelo,                       
                       destino='precSatONS/test_precSatONS.jpg'
                       )
    

if __name__ == '__main__':
    exemploTxtsONS()
    exemploCPTEC(modelo='WRF')
    exemploSateliteONS()