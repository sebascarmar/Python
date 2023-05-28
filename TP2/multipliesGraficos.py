# Grafica en la misma pagina, sino abre una ventana con qt5
#%matplotlib inline
#%matplotlib qt5


import numpy as np
import matplotlib.pyplot as pl


def figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, show="False"):

    pl.figure(figsize=[14,14])
    pl.figure(numplot)
    for i in range(len(x)):
        pl.subplot(row, col, joinVec[i])
        
        if( typeGraf[i]=='p' ):
            pl.plot(x[i], y[i])
        else:
            pl.stem(x[i], y[i])
        
        pl.xlim( xlim[i] )
        pl.ylim( ylim[i] )
        
        pl.ylabel(xlabel)
        pl.xlabel(ylabel)

    if( show=="true" ):
        pl.show()
    


x = np.array([])
for i in range(4): #Esto sería para 4 gráficos
    x = np.append(x, np.arange(0.,2.,0.01))

phase = 0.
freq = 1.
y = np.array([])
for i in range(4): #Esto sería para 4 gráficos
    y = np.append(y, np.sin(2.*np.pi*freq*x + phase))
    phase += np.pi/10.
    freq += 1.

print(y)

row = 3
col = 3

joinVec=((1,2),3,(4,5,6),(7,8,9))

numplot=1

typeGraf=['s','p','p','s']

xlim = [[0.,2.], [0.,2.], [0.,2.], [0.,2.]]
ylim = [[-2.,2.], [-2.,2.], [-2.,2.], [-2.,2.]]

xlabel = "Amplitud"
ylabel = "Tiempo"

figPlot(x, y, row, col, joinVec, numplot, typeGraf, xlim, ylim, xlabel, ylabel, "true")



##define las dimensiones de las figuras por defecto (en pulgadas)
#pl.rcParams['figure.figsize']= [16.0,10.0]
#
#
#
### Graficos usando matplotlib.pyplot
#phase0 = 0.
#phase1 = np.pi/2.
#f0     = 2.
#f1     = 2.
#f2     = 4.
#
#t  = np.arange(0.,f0,0.01)
#y0 = np.sin(2.*np.pi*f0*t + phase0)
#y1 = np.sin(2.*np.pi*f1*t + phase1)
#y2 = np.cos(2.*np.pi*f2*t + phase0)
#
#
#
#pl.figure(figsize=[14,14])
#
#pl.subplot(3,3,(1,3))
#pl.plot(t,y0,'.-',linewidth=2.0,label='Phase: %1.2f'%phase0)
#pl.ylabel('Amplitud')
#pl.xlabel('Tiempo')
#pl.legend()
#pl.grid()
#
#pl.subplot(3,3,(4,7))
#pl.plot(t,y1,'rx-',linewidth=1.0,label='Phase: %1.2f'%phase1)
#pl.ylabel('Amplitud')
#pl.xlabel('Tiempo')
#pl.legend()
#pl.grid()
#
#pl.subplot(3,3,5)
#pl.stem(t,y2,'y',markerfmt='C1o')
#pl.plot(t,y2,'g',linewidth=1.0,label='Phase: %1.2f'%phase0)
#pl.ylabel('Amplitud')
#pl.xlabel('Tiempo')
#pl.xlim(0,0.5)
#pl.legend()
#pl.grid()
#
#pl.subplot(3,3,6)
#pl.plot(t,y1,'.',linewidth=1.0,label='Phase: %1.2f'%phase1)
#pl.ylabel('Amplitud')
#pl.xlabel('Tiempo')
#pl.legend()
#pl.grid()
#
#pl.subplot(3,3,(8,9))
#pl.plot(t,y1,'m+-',linewidth=1.0,label='Phase: %1.2f'%phase1)
#pl.ylabel('Amplitud')
#pl.xlabel('Tiempo')
#pl.legend()
#pl.grid()
#pl.title('Sin')
#
### Guardando figuras en archivos
#pl.savefig('grafica.eps')
#pl.savefig('grafica.pdf')
#pl.savefig('grafica.png')
#
#pl.show()
