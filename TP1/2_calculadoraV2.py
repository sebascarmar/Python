
import numpy as np

# Imprime menú principal.
print("********************* CALCULADORA *********************")
print("\t1-Sumar \n\t2-Restar \n\t3-Multiplicar \n\t4-Dividir \n\t5-Iterativo \n\t6-Producto punto")

# Ingreso de opción principal. Además formateado como int
opcion = int( input("Ingrese una opción: ") )


if( opcion==1 or opcion==2 or opcion==3 or opcion==4 ):# Ingreso de operandos para las operaciones no iterativas.
    a = int( input("\nIngrese a=") )
    b = int( input("Ingrese b=") )

elif( opcion==5 ):# Opción de iteración.
    # Imprime submenú de iteración.
    print("\n\tDesea:\n\t\ta-Sumar \n\t\tb-Restar \n\t\tc-Multiplicar")
    opcionIter = input("Ingrese una opcion: ")

    # Termina ejecución si la opción para el submenú es inválida.
    if( not(opcionIter=='a' or opcionIter=='b' or opcionIter=='c') ):
        print("Opción inválida")
        exit()
    
    # Ingreso de operandos para operaciones iterativas. También  formatea como int.
    a = int( input("\nIngrese step=") )
    b = int( input("Ingrese iter=") )

elif( opcion==6 ):
    # Imprime submenú de producto punto.
    print("\n\tDesea operar con:\n\t\ta-Vectores \n\t\tb-Matrices")
    opcionProdPunto = input("Ingrese una opcion: ")

    # Termina ejecución si la opción para el submenú es inválida.
    if( not(opcionProdPunto=='a' or opcionProdPunto=='b') ):
        print("Opción inválida")
        exit()

    if( opcionProdPunto=='a' ):
        a = input("\nIngrese, separado por comas, el vector a=")
        b = input("Ingrese, separado por comas, el vector b=")
    else:
        print("En construcción")

    #COMO CARGAR UN ARRAY BIDIMENSIONAL EN PYTHON
    #REVISAR LOS 3 MODIFICADORES DE FORMATO VISTOS EN CLASE

else:# Termina ejecución si la opción para el menú es inválida.
    print("Opción inválida")
    exit()



import numpy as np


# Imprime resultados.
if( opcion==1 ):
    print("Su resultado es: a+b=%d" %(a+b))
elif( opcion==2 ):
    print("Su resultado es: a-b=%d" %(a-b))
elif( opcion==3 ):
    print("Su resultado es: a*b=%d" %(a*b))
elif( opcion==4 ):
    print("Su resultado es: a/b=%f" %float(a/b))
elif( opcion==5 ):
    
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

elif( opcion==6 ):

    if( opcionProdPunto=='a' ):
        # Pasaje de string a vector de string.
        a = a.split(',')
        b = b.split(',')
        
        # Validación de tamaños de los vectores.
        if( len(a)!=len(b) ):
            print("Los tamaños de los vectores no son iguales.")
            exit()
        
        # Pasaje de string a int.
        for i in range(len(a)):
            a[i] = int(a[i])
            b[i] = int(b[i])
        
        # Cálculo e impresión del resultado.
        productoPunto = np.dot(np.array(a),np.array(b))
        print('El resultado es: a.b =', productoPunto)
        
    else:
        print("En contstrucciń")

