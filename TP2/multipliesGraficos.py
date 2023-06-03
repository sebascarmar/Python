# Grafica en la misma pagina, sino abre una ventana con qt5
#%matplotlib inline
#%matplotlib qt5


import numpy as np
import matplotlib.pyplot as pl


def figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, show="False"):

    pl.figure(figsize=[14,14])
    pl.figure(numplot)
    for i in range(4):
        pl.subplot(row,col,joinVec[i])
        
        if( typeGraf[i]=='p' ):
            pl.plot(x[i], y[i], linewidth=1.0,)
        else:
            pl.stem(x[i], y[i])
        
        pl.xlim(xlim[i])
        pl.ylim(ylim[i])
        
        pl.ylabel(ylabel)
        pl.xlabel(xlabel)
        
        pl.grid()


    if( show=="true" ):
        pl.show()
    

###########################################################################################


row = int(input("Ingrese el número de filas: "))
col = int(input("Ingrese el número de columnas: "))

##################################################### INGRESO DE joinVec #################################################
##########################################################################################################################
ingreseOtraVez = 1
while( ingreseOtraVez == 1 ):
    # Paso 1: Solicitar al usuario los elementos de la tupla anidada
    ingresoAgrupaciones = input("\nIngrese las ubicaciones de los subplots separadas por comas, y las celdas unificadas separadas por espacios: ")
    
    # Paso 2: Dividir los elementos ingresados por comas y almacenarlos en una lista
    listaAgrupaciones = ingresoAgrupaciones.split(",")
    
    # Paso 3: Crear una lista para almacenar las tuplas internas
    tuplaInternaAgrupaciones = []
    
    # Paso 4: Recorrer la lista de elementos y dividir cada elemento interno por espacios para crear las tuplas internas
    #         y convertir los elementos individuales en enteros
    for elementoLista in listaAgrupaciones:
        valores = elementoLista.split()
        if len(valores) > 1:
            tuplaAux = tuple(int(aux) for aux in valores)
            tuplaInternaAgrupaciones.append(tuplaAux)
        else:
            elementoInt = int(valores[0])
            tuplaInternaAgrupaciones.append(elementoInt)
    
    # Paso 5: Convertir la lista de tuplas internas en una tupla anidada
    joinVec = tuple(tuplaInternaAgrupaciones)
    
    # Imprimir la tupla anidada resultante
    #print("La tupla anidada ingresada es:", joinVec)
    #print(len(joinVec))
    
    
    ############################### VALIDACION DEL joinVec ###################################################33
    ingreseOtraVez=0
    cumpleCond1=True
    cumpleCond2=True
    cumpleCond3=True

    if( len(joinVec)>(row*col) ): #cantidad de elementos debe ser menor o igual al máximo (row*col)
        print("\nLa cantidad de gráficos requeridos supera la capacidad máxima de subplots ({}).".format(row*col),end=" ")
        ingreseOtraVez=1
        cumpleCond1=False
  
    if( cumpleCond1==True ): # Controla que ningún número de ubicación supere al máximo posible.
       
        for aux in joinVec:
            
            if( isinstance(aux, tuple) ): # Si es tupla.
                
                if( len(aux) <= 2 ): # si la agrupación de un gráfico es de solo dos elementos
                    
                    for aux2 in aux:
                        if( aux2 > (row*col) ):
                            print("\nValor de ubicación de suplot supera el máximo: {}.".format(aux),end=" ")
                            ingreseOtraVez=1
                            cumpleCond2=False
                            break

                else:                # No permite que se ingresen agrupaciones de más de 2 elementos.
                    print("\nLa agrupación se expresa solo con dos ubicaciones (max y min), no como: {}.".format(aux),end=" ")
                    ingreseOtraVez=1
                    cumpleCond2=False
             
            else:                         # Si es int. 
                
                if( aux > (row*col) ):
                    print("\nValor de ubicación de suplot supera el máximo: {}.".format(aux),end=" ")
                    ingreseOtraVez=1
                    cumpleCond2=False
                    break
   
    if( cumpleCond2==True ): # Controla que las ubicaciones no sean repetiadas.
       
        arrayAux = np.arange(1, row*col+1 , 1)
        
        for aux in joinVec:
            
            if( isinstance(aux, tuple) ): # Si es tupla.
                
                for aux2 in aux:
                    contador=1
                    for i in range(len(arrayAux)):
                        if( aux2 == arrayAux[i] ):
                            arrayAux[i]=0
                            break # Sin este continua iterando y al final entra en la otra condición aunque se correcta la tupla
                        elif( contador == len(arrayAux) ):
                            print("\nUbicación repetida: {}.".format(aux),end=" ")
                            ingreseOtraVez=1
                            cumpleCond3=False
                            break
                        
                        contador+=1
             
            else:                         # Si es int. 
                contador=1
                for i in range(len(arrayAux)):
                    if( aux == arrayAux[i] ):
                        arrayAux[i]=0
                        break
                    elif( contador == len(arrayAux) ):
                        print("\nUbicación repetida: {}.".format(aux),end=" ")
                        ingreseOtraVez=1
                        cumpleCond3=False
                        break
                    
                    contador+=1
            
        




#joinVec=((1,2),3,(4,6),(7,9))


##########################################################################################################################

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


##########################################################################################################################

numplot = int(input("\nIngrese el identificador numplot="))

##########################################################################################################################

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
#typeGraf=['s','p','p','s']

typeGraf = ingresoYValidacionTiposDeGraficos( len(joinVec) )
##########################################################################################################################

xlim = ((0.,1.), (0.,2.), (0.,2.), (0.,0.5))
ylim = ((-2.,2.), (-2.,2.), (-2.,2.), (-2.,2.))

xlabel = "Tiempo"
ylabel = "Amplitud"

figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, "true")

