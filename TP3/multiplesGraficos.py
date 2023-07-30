############################################################################################
#                             IMPORTACION DE BIBLIOTECAS                                  ##
############################################################################################

import numpy as np
import matplotlib.pyplot as pl



############################################################################################
#                          DEFINICIÓN DE FUNCIONES                                        ##
############################################################################################

def graficar( ):
    print("********************* MULTI-PLOT **********************")

    #********** Ingreso de la cantidad de filas y columndas de la Figura **********************#
    
    row = int(input("Ingrese el número de filas: "))
    col = int(input("\nIngrese el número de columnas: "))
    
    
    #********************** Ingreso y validacion del joinVec **********************************#
    
    cumpleCond1=False
    cumpleCond2=False
    cumpleCond3=False
    while( cumpleCond1==False or cumpleCond2==False or cumpleCond3==False ):
    
        joinVec = ingresoDelJoinVec(  )
        
        ingreseOtraVez=0
        cumpleCond1=True
        cumpleCond2=True
        cumpleCond3=True
    
        cumpleCond1 = validaCantidadDeGraficasMenorACeldasTotales( joinVec, row, col, cumpleCond1 )
      
        if( cumpleCond1==True ): # Controla que ningún número de ubicación supere al máximo posible.
            cumpleCond2 = validaUbicacionNoSupereElMaximoPosible( joinVec, row, col, cumpleCond2 )
       
        if( cumpleCond1==True and cumpleCond2==True ): # Controla que las ubicaciones no sean repetiadas.
            cumpleCond3 = validaUbicacionesNoRepetidas( joinVec, row, col, cumpleCond3 )
    
    
    #********************* Generación de los valores de x e y para graficar ********************#
    
    x = []
    for i in range(len(joinVec)): #Esto sería para 4 gráficos
        x.append(np.arange(0.,5.,0.01))
    
    
    phase = 0.
    freq = 1.
    y=[]
    for i in range(len(x)): #Esto sería para 4 gráficos
        auxY=np.sin(2.*np.pi*freq*x[0] + phase)
        phase += np.pi/10.
        freq += 1.
        y.append(auxY)
    
    
    #********************* Ingreso del identificador de la figura ******************************#
    
    numplot = int(input("\nIngrese el identificador numplot="))
    
    
    #********************* Ingreso y validación de los tipos de gráficos ***********************#
    
    typeGraf = ingresoYValidacionTiposDeGraficos( len(joinVec) )
    
    
    #************** Ingreso y validación de los rangos de los ejes a mostrar *******************#
    
    ingreseRangosXDeNuevo = True
    while( ingreseRangosXDeNuevo==True ):
        xlim = ingresoDeLimitesDeEje("x")
        ingreseRangosXDeNuevo = validaRangosDeEje(xlim, len(joinVec))
    
    ingreseRangosYDeNuevo = True
    while( ingreseRangosYDeNuevo==True ):
        ylim = ingresoDeLimitesDeEje("y")
        ingreseRangosYDeNuevo = validaRangosDeEje(ylim, len(joinVec))
    
    
    #*********************** Ingreso de las etiquietas de los ejes *****************************#
    
    xlabel = input("\nIngrese la etiqueta del eje horizontal: ")
    ylabel = input("\nIngrese la etiqueta del eje vertical: ")
    
    
    #********************* Ingreso de habilitación para ver el gráfico o no ********************#
    
    ingresoShowGraph = input("\nIngrese si desea mostrar la figura (Si o No): ")
    if( ingresoShowGraph.lower()=='si' ):
        show = True
    else:
        show = False

    listaParametros = [x,y,row,col,joinVec,numplot,typeGraf, xlim,ylim,xlabel,ylabel,show]

    return listaParametros

    
def ingresoDelJoinVec( ):
    ingresoAgrupaciones = input("\nIngrese las ubicaciones de los subplots separadas por comas, y las celdas unificadas separadas por espacios: ")
    
    listaAgrupaciones = ingresoAgrupaciones.split(",")
    
    tuplaInternaAgrupaciones = []
    
    for elementoLista in listaAgrupaciones: # Recorre lista elemento a elemento
        valores = elementoLista.split()
        if len(valores) > 1: # Si elelemento es una tupla de más de 1 elemento.
            tuplaAux = tuple(int(aux) for aux in valores)
            tuplaInternaAgrupaciones.append(tuplaAux)
        else:                # Si el elemento es un int.
            elementoInt = int(valores[0])
            tuplaInternaAgrupaciones.append(elementoInt)
    
    # Convierte la lista de tuplas internas en una tupla anidada.
    joinVecAux = tuple(tuplaInternaAgrupaciones)

    return joinVecAux


def validaCantidadDeGraficasMenorACeldasTotales( joinVec, row, col, cumpleCond1Aux ):
    if( len(joinVec)>(row*col) ): #cantidad de elementos debe ser menor o igual al máximo (row*col)
        print("\nLa cantidad de gráficos requeridos supera la capacidad máxima de subplots ({}).".format(row*col),end=" ")
        cumpleCond1Aux=False

    return cumpleCond1Aux


def validaUbicacionNoSupereElMaximoPosible( joinVec, row, col, cumpleCond2Aux ):
    for aux in joinVec:
        
        if( isinstance(aux, tuple) ): # Si es tupla.
            
            if( len(aux) <= 2 ): # si la agrupación de un gráfico es de solo dos elementos
                
                for aux2 in aux:
                    if( aux2 > (row*col) ):
                        print("\nValor de ubicación de suplot supera el máximo: {}".format(aux),end=" ")
                        cumpleCond2Aux=False
                        break
                
            else:                # No permite que se ingresen agrupaciones de más de 2 elementos.
                print("\nLa agrupación se expresa solo con dos ubicaciones (max y min), no como: {}".format(aux),end=" ")
                cumpleCond2Aux=False
         
        else:                         # Si es int. 
            
            if( aux > (row*col) ):
                print("\nValor de ubicación de suplot supera el máximo: {}".format(aux),end=" ")
                cumpleCond2Aux=False
                break

    return cumpleCond2Aux


def validaUbicacionesNoRepetidas( joinVec, row, col, cumpleCond3Aux ):
   
    arrayAux = np.arange(1, row*col+1 , 1)
    
    for aux in joinVec:
        
        if( isinstance(aux, tuple) ): # Si es tupla.
            
            for aux2 in aux:
                contador=1
                for i in range(len(arrayAux)):
                    if( aux2 == arrayAux[i] ):
                        arrayAux[i]=0
                        break # Sin este continua iterando y al final entra en la otra condición aunque sea correcta la tupla
                    elif( contador == len(arrayAux) ):
                        print("\nUbicación repetida: {}".format(aux),end=" ")
                        cumpleCond3Aux=False
                        break
                    
                    contador+=1
         
        else:                         # Si es int. 
            contador=1
            for i in range(len(arrayAux)):
                if( aux == arrayAux[i] ):
                    arrayAux[i]=0
                    break
                elif( contador == len(arrayAux) ):
                    print("\nUbicación repetida: {}".format(aux),end=" ")
                    cumpleCond3Aux=False
                    break
                
                contador+=1
    
    return cumpleCond3Aux


def ingresoYValidacionTiposDeGraficos( lenJoinVec ):
    
    tiposDeGraficosCorrectos = False
    while( tiposDeGraficosCorrectos==False ):
     
        ingresoTiposDeGraf = input("\nIngrese los tipos de graficos separado por comas (s:stem y p:plot): ")
        typeGrafAux = ingresoTiposDeGraf.split(",")
     
        if( len(typeGrafAux)==lenJoinVec ): # Verifica que la cantidad de elem. ingresados se corresponda con la cant. de graf.
            
            for tipoIndividual in typeGrafAux:   # Recorre lo ingresado para detectar algún tipo de gráfico erróneo.
                
                if( tipoIndividual=='s' or tipoIndividual=='p' ):
                    tiposDeGraficosCorrectos=True
                else:
                    print("\nTipo de gráfico no válido:",tipoIndividual,end="")
                    tiposDeGraficosCorrectos=False
                    break
            
        else:
            print("\nDebe ingresar {} tipos de gráficos.".format(lenJoinVec),end=" ")

    return typeGrafAux


def ingresoDeLimitesDeEje( nombreEje ):
    ingresoRangos = input("\nIngrese los extremos del eje {} separados por espacios. Separe con comas cada par: ".format(nombreEje))

    listaDeRangos = ingresoRangos.split(",")

    tuplaInternaRangos = []

    for elementoLista in listaDeRangos:
        valorFlotante = elementoLista.split()
        tuplaAux = tuple(float(aux) for aux in valorFlotante)
        tuplaInternaRangos.append( tuplaAux )

    limitesEje = tuple( tuplaInternaRangos )

    return limitesEje


def validaRangosDeEje( limitesDeEje, lenJoinVec ):

    if( len(limitesDeEje)==lenJoinVec ): # Verifica que el número de rangos ingresados se corresponda con el núm. de gráficos.

        for rango in limitesDeEje:
            if( len(rango)==2 ): # Verifcia que cada rango para verificar que tengo límite superior e inferior.
                flagAux = False
            else:                # Si no posee dos límites, no valida.
                print("\nCada rango debe poseer 2 elementos (extremo inf y sup)",end="")
                flagAux = True
                break
    else:                                # Si no coincide con el número de gráficos, no valida.
        print("\nLa cantidad de rangos que debe ingresar es: {}".format(lenJoinVec),end="")
        flagAux = True

    return flagAux


def figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, show=False):

    pl.figure(figsize=[14,14])
    pl.figure(numplot)
    for i in range(len(joinVec)):
        pl.subplot(row,col,joinVec[i])
        
        if( typeGraf[i]=='p' ):
            pl.plot(x[i], y[i], linewidth=1.0,)
        else:
            pl.stem(x[i], y[i])
        
        pl.xlim(xlim[i])
        pl.ylim(ylim[i])
        
        pl.grid()
        
        # Selecciona la ubicación del subplot para saber si corresponde poner xlabel o ylabel.
        if( isinstance(joinVec[i],tuple) ):
            auxTupla = joinVec[i]
            celdaUbi = auxTupla[0]
        else:
            celdaUbi = joinVec[i]
        
        # Define si corresponde la ylabel para el subplot en particular.
        mod = celdaUbi%col
        if( mod==1 ):
            pl.ylabel(ylabel)
        
        # Define si corresponde la xlabel para el subplot en particular.
        filaInfMin = col*(row-1)+1
        filaInfMax = row*col
        if(  (celdaUbi>=filaInfMin) and (celdaUbi<=filaInfMax) ): 
            pl.xlabel(xlabel)


    if( show==True ):
        pl.show()



############################################################################################
#                                PROGRAMA PRINCIPAL                                       ##
############################################################################################

def start():
    parametrosParaGraficar = graficar( )
    
    x       = parametrosParaGraficar[0]
    y       = parametrosParaGraficar[1]
    row     = parametrosParaGraficar[2]  
    col     = parametrosParaGraficar[3]
    joinVec = parametrosParaGraficar[4]
    numplot = parametrosParaGraficar[5]
    typeGraf= parametrosParaGraficar[6]
    xlim    = parametrosParaGraficar[7]
    ylim    = parametrosParaGraficar[8]
    xlabel  = parametrosParaGraficar[9]
    ylabel  = parametrosParaGraficar[10]
    show    = parametrosParaGraficar[11]
    
    
    
    figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, show)
    
    
