# Imprime menú principal.
print("******** CALCULADORA ********")
print("\t1-Sumar \n\t2-Restar \n\t3-Multiplicar \n\t4-Dividir \n\t5-Iterativo")

# Ingreso de opción principal. Además formateado como int
opcion = int( input("Ingrese una opción: ") )


if( opcion==1 or opcion==2 or opcion==3 or opcion==4 ):# Ingreso de operandos para las operaciones no iterativas.
    a = int( input("\nIngrese a=") )
    b = int( input("Ingrese b=") )

elif(opcion==5):# Opción de iteración.
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

else:# Termina ejecución si la opción para el menú es inválida.
    print("Opción inválida")
    exit()


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
