print("******** CALCULADORA ********")
print("\t1-Sumar \n\t2-Restar \n\t3-Multiplicar \n\t4-Dividir \n\t5-Iterativo")

opcion = int(input("\nIngrese una opción: "))

if(opcion==1 or opcion==2 or opcion == 3 or opcion==4):
    a = int(input("Ingrese a="))
    b = int(input("Ingrese b="))
elif(opcion==5):
    print("\tDesea:\n\t\ta-Sumar \n\t\tb-Restar \n\t\tc-Multiplicar")
    opcionIter = input("\nIngrese una opcion: ")

    if(not(opcionIter == 'a' or opcionIter == 'b' or opcionIter == 'c')):
        print("Opción inválida")
        exit()

    a = int(input("Ingrese step="))
    b = int(input("Ingrese iter="))
else:
    print("Opción inválida")
    exit()

if(opcion == 1):
    print("Su resultado es: a+b=%d" %(a+b))
elif(opcion ==2):
    print("Su resultado es: a-b=%d" %(a-b))
elif(opcion ==3):
    print("Su resultado es: a*b=%d" %(a*b))
elif(opcion ==4):
    print("Su resultado es: a/b=%f" %float(a/b))
elif(opcion==5):
    
    if(opcionIter=='a'):
        resultado = 0
        
        for i in range(b):
            resultado += a
            if(i< (b-1)):
                print(a,end='+')
            else:
                print(a,end=' =')

    if(opcionIter=='b'):
        resultado = a
        
        for i in range(b):
            resultado -= a
            if(i< (b-1)):
                print(a,end='-')
            else:
                print(a,end=' =')

    if(opcionIter=='c'):
        resultado = 1
        
        for i in range(b):
            resultado *= a
            if(i< (b-1)):
                print(a,end='*')
            else:
                print(a,end=' =')


    print(" %d" %resultado)
