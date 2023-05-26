
import numpy as np
from os import system, name 


def clear(): 
    if name == 'nt': 
        x = system('cls') 
    else: 
        x = system('clear') 

def ingresoMatriz(name):
    aux='0'
    i=0
    listaFilas = []
    tamañoPrimerVector = 0
    
    print("\nIngrese separando por comas ('x' para terminar)")
    while( aux!='x' ):
        print('\tVector', name, end='')
        aux = input('%d=' %i)
     
        if( aux!='x'):
            # Pasaje de lista a vector de string.
            aux = aux.split(',')
            
            # Pasaje de lista de string a lista de int.
            for j in range(len(aux)):
                aux[j] = int(aux[j])
            
            # Almacena el tamaño de la 1er lista ingresada.
            if( i==0 ):
                tamañoPrimerVector = len(aux)
            
            # Impide que se ingrese un nuevo elemento a la lista si es de disnto tamaño.
            if( tamañoPrimerVector==len(aux) ):
             
                listaFilas.append(aux)
                
                vector = np.array([np.array(k) for k in listaFilas])
             
                i+=1
            
            else:
                    print("\tEl tamaño del vector debe ser igual al primero ingresado")
 
    return vector


# Imprime menú principal.
print("********************* CALCULADORA *********************")
print("\t1-Sumar \n\t2-Restar \n\t3-Multiplicar \n\t4-Dividir \n\t5-Iterativo \n\t6-Producto punto")

# Ingreso de opción principal. Además formateado como int
opcion = int( input("Ingrese una opción: ") )


if( opcion==1 or opcion==2 or opcion==3 or opcion==4 ):# Ingreso de operandos para las operaciones no iterativas.
    a = int( input("\nIngrese a=") )
    b = int( input("Ingrese b=") )

elif( opcion==5 ):# Opción de iteración.
    # Limpieza de pantalla.
    clear()

    # Imprime submenú de iteración.
    print("Desea iterar con:\n\t\ta-Sumar \n\t\tb-Restar \n\t\tc-Multiplicar")
    opcionIter = input("Ingrese una opcion: ")

    # Termina ejecución si la opción para el submenú es inválida.
    if( not(opcionIter=='a' or opcionIter=='b' or opcionIter=='c') ):
        print("Opción inválida")
        exit()
    
    # Ingreso de operandos para operaciones iterativas. También  formatea como int.
    a = int( input("\nIngrese step=") )
    b = int( input("Ingrese iter=") )

elif( opcion==6 ):
    # Limpieza de pantalla.
    clear()

    # Imprime submenú de producto punto.
    print("Desea realizar el producto punto entre:\n\t\ta-Vectores \n\t\tb-Matrices")
    opcionProdPunto = input("Ingrese una opcion: ")

    # Termina ejecución si la opción para el submenú es inválida.
    if( not(opcionProdPunto=='a' or opcionProdPunto=='b') ):
        print("Opción inválida")
        exit()

    if( opcionProdPunto=='a' ):# Producto punto entre vectores.
        
        vectoresMismoTamaño=0
        while( vectoresMismoTamaño==0 ):
            a = input("\nIngrese, separado por comas, el vector a=")
            b = input("Ingrese, separado por comas, el vector b=")
            
            # Pasaje de lista a vector de string.
            a = a.split(',')
            b = b.split(',')
            
            # Validación de tamaños de los vectores.
            if( len(a)!=len(b) ):
                print("Los tamaños de los vectores no son iguales.")
            else:
                vectoresMismoTamaño=1
        
        # Pasaje de lista de string a lista de int.
        for i in range(len(a)):
            a[i] = int(a[i])
            b[i] = int(b[i])
        
    else:                      # Producto punto entre matrices.
        matricesDimensionesCompatibles=0
        while( matricesDimensionesCompatibles==0 ):
            a = ingresoMatriz('a')
            b = ingresoMatriz('b')
         
            if( len(a)!=len(b[0]) ):
                print("Los dimensiones de las matrices (m1xn1 y n2xm2) no son compatibles (m1!=m2).")
            elif( len(a[0])!=len(b) ):
                print("Los dimensiones de las matrices (m1xn1 y n2xm2) no son compatibles (n1!=n2).")
            else:
                matricesDimensionesCompatibles=1
        
       # resultado = np.dot(a, a)
       # print(resultado)
       # matrix1 = np.asmatrix(a)
       # print(type(a))
       # print(a)
       # print(type(matrix1))
       # print(matrix1)
       # print("En construcción")
       # resultado = np.dot(matrix1, matrix1)
       # print(resultado)

    #COMO CARGAR UN ARRAY BIDIMENSIONAL EN PYTHON
    #REVISAR LOS 3 MODIFICADORES DE FORMATO VISTOS EN CLASE

else:# Termina ejecución si la opción para el menú es inválida.
    print("Opción inválida")
    exit()


# Imprime resultados.
if( opcion==1 ):# Suma.
    print("Su resultado es: a+b=%d" %(a+b))
elif( opcion==2 ):# Resta.
    print("Su resultado es: a-b=%d" %(a-b))
elif( opcion==3 ): # Multiplicación.
    print("Su resultado es: a*b=%d" %(a*b))
elif( opcion==4 ):# División
    print("Su resultado es: a/b=%f" %float(a/b))
elif( opcion==5 ): #Iteración.
    
    print("Su resultado es:", end=" ")
    if( opcionIter=='a' ):# Iteración de suma.
        resultado = 0
        
        for i in range(b):
            resultado += a
            if( i<(b-1) ):
                print(a,end='+')
            else:
                print(a,end='=')

    if( opcionIter=='b' ):# Iteración de la resta.
        resultado = a
        
        for i in range(b):
            resultado -= a
            if( i<(b-1) ):
                print(a,end='-')
            else:
                print(a,end='=')

    if( opcionIter=='c' ):# Iteración de la multiplicación.
        resultado = 1
        
        for i in range(b):
            resultado *= a
            if( i<(b-1) ):
                print(a,end='*')
            else:
                print(a,end='=')

    print("%d" %resultado)

elif( opcion==6 ):# Producto punto.

    if( opcionProdPunto=='a' ):# Producto punto entre vectores.
        
        # Cálculo e impresión del resultado.
        productoPunto = np.dot(np.array(a),np.array(b))
        print('El resultado es: a.b =', productoPunto)
        
    else:                      # Producto punto entre matrices.
        print("En contstrucciń")

