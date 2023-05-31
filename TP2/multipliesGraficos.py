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

x = []
for i in range(4): #Esto sería para 4 gráficos
    x.append(np.arange(0.,2.,0.01))


phase = 0.
freq = 1.
y=[]
for i in range(len(x)): #Esto sería para 4 gráficos
    auxY=np.sin(2.*np.pi*freq*x[0] + phase)
    phase += np.pi/10.
    freq += 1.
    y.append(auxY)

row = int(input("Ingrese el número de filas: "))
col = int(input("\nIngrese el número de columnas: "))

##################################################### INGRESO DE joinVec #################################################
##########################################################################################################################
# Paso 1: Solicitar al usuario los elementos de la tupla anidada
ingresoAgrupaciones = input("Ingrese los elementos de la tupla anidada separados por comas y los elementos internos separados por espacios: ")

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
print("La tupla anidada ingresada es:", joinVec)
print(len(joinVec))


############################### VALIDACION DEL joinVec ###################################################33
if( len(joinVec)>=(row*col) ): #cantidad de elementos debe ser menor o igual al máximo (row*col)
    ingreseOtraVez=1
    
else: #acceso a cada elemento de las agrupaciones. Se debe ver si son repetidos y si son horizontales
    for aux in joinVec:
        if( isinstance(aux, tuple) ):
            if( len(aux) > 1 ):
                for aux2 in aux:
                    print(aux2)
        else:
            print(aux)
    



#joinVec=((1,2),3,(4,6),(7,9))


##########################################################################################################################



numplot=1

typeGraf=['s','p','p','s']

xlim = ((0.,1.), (0.,2.), (0.,2.), (0.,0.5))
ylim = ((-2.,2.), (-2.,2.), (-2.,2.), (-2.,2.))

xlabel = "Tiempo"
ylabel = "Amplitud"

figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, "true")

