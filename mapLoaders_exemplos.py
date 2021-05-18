# -*- coding: utf-8 -*-

"""
******************************************************************************
Rotinas de exemplo do uso do módulo 'mapLoaders'
              
Autor   : Nelson Rossi Bittencourt
Versão  : 0.1
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
            fileName = '{}/{}/{}_{}.dat'.format(dirEntrada,nomeModelo, nomeModelo,dia)
            
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
                                titulo='Modelo {}\nDia {}'.format(nomeModelo,dia),
                                lons=lons,
                                lats=lats,
                                dados=chuva,
                                modeloMapa=mapaModelo,
                                destino='{}/{}_fig_dia_{}.jpg'.format(dirSaida, nomeModelo,dia)
                                )

        # Plota o mapa com a soma de todos os dias.
        plotMap.plotarMapa(
                            titulo='Modelo {}\nSoma dos {} dias'.format(nomeModelo,numDias),
                            lons=lons,
                            lats=lats,
                            dados=chuvaTotal,
                            modeloMapa=mapaModelo,
                            destino='txtsONS/Saida/{}_fig_total.jpg'.format(nomeModelo)
                            )


def exemploEtaCPTEC():
    """
    Lê arquivos tipo 'grib' com precipitações previstas através do modelo ETA.
    Estes arquivos são disponibilizados pelo CPTEC em sua área FTP.

    Este exemplo, com pequenas alterações, poderá ser utilizado para os demais modelos 
    que o CPTEC utiliza (WRF e BAM).

    """

    # Flag para determina se serão plotados os mapas horários (True) ou não (False).
    flagPlotaDiario = True

    # Cria um objeto 'Mapa', com o modelo de mapa, para uso no plotMap.
    mapaModelo = plotMap.loadMapTemplate('template/ChuvaPrevistaONS.dat')

    # Variável que conterá o somatório das chuvas diárias.
    chuvaTotal =  0
    
    # Hora e dia iniciais.
    hora = 12
    dia = 18

    # Cria uma string para o dia inicial, considerando o formato da 'string' do arquivo original do modelo.
    sDia0 = f'{dia:02d}'

    # Loop para o número de períodos (no caso do ETA, 24 horas).
    for i in range(24):                                                       
        
        sHora = f'{hora:02d}'           # String com a hora formatada.
        sDia = f'{dia:02d}'             # String com o dia formatado.

        # Nome do arquivo do modelo ETA        
        fileName = 'eta40_CPTEC/Entrada/eta_40km_202105{}00+202105{}{}.grb'.format(sDia0,sDia,sHora)        
        
        # Em testes. Nome do arquivo WRF.
        #fileName = 'WRF_CPTEC/Entrada/WRF_cpt_05KM_202105{}00_202105{}{}.grib2'.format(sDia0,sDia,sHora)

        hora = hora + 1                 # Incrementa a hora.

        # Caso o contador de horas atinja 24, reinicia o contador de horas e incrementa o contador a variável 'dia'.
        if (hora == 24):
            hora = 0
            dia = dia + 1

        # Obtem os valores do arquivo 'grib' do ETA.
        lons, lats, chuva = mapLoaders.chuvaEtaCPTEC(fileName,14,1000)
        
        # Em testes. Obtem os valores valor do modelo WRF do CPTEC.
        # Nos testes estou utilizando cortes só com a precipitação, por isso a mensagem do arquivo 'grib2' é igual a 1.
        #lons, lats, chuva = mapLoaders.chuvaEtaCPTEC(fileName,1,1/24)
        
        # Acumulador de chuva.
        chuvaTotal = chuvaTotal + chuva

        # Plota mapa para cada período (caso flagPlotaDiario = True).
        if (flagPlotaDiario):
            plotMap.plotarMapa(
                               titulo='Modelo ETA CPTEC Grib\nDia {} - Hora {}'.format(sDia,sHora),
                               lons=lons,
                               lats=lats,
                               dados=chuva,
                               modeloMapa=mapaModelo,
                               destino='eta40_CPTEC/ETA_CPTEC_grib_{}{}'.format(sDia,sHora) + '.jpg'
                               )

    # Plota mapa com valor acumulado.
    plotMap.plotarMapa(
                        titulo='Modelo ETA CPTEC Grib\nSomatório das Horas',
                        lons=lons,
                        lats=lats,
                        dados=chuvaTotal,
                        modeloMapa=mapaModelo,
                        destino='eta40_CPTEC/Saida/ETA_CPTEC_grib_Total.jpg'
                        )

if __name__ == '__main__':
    exemploTxtsONS()
    exemploEtaCPTEC()