
import numpy as n
def lineal(vProblema):
    archivo = open("pre-procesados/pokes_test_binariz.txt")
    contenido = archivo.readlines()

    X = contenido[3:3+int(contenido[1])]
    X = [i.split("\t") for i in X]
    X = [list(map(float, i)) for i in X]

    Y = contenido[3+int(contenido[1]):]
    Y = [i.split("\t") for i in Y]
    Y = [list(map(float, i)) for i in Y]

    X = n.array(X)
    Y = n.array(Y)

    Paso1 = X.dot(X.T)
    Paso2 = n.linalg.inv(Paso1)
    Xpseudo = X.T.dot(Paso2)

    W = Y.dot(Xpseudo)

    #print("X:")
    #print(X)

    #print("Y:")
    #print(Y)

    #print("W:")
    #print(W)

    #################################################################################################
    #################################################################################################
    ### EVALUACION DE LOS CASOS DE PRUEBA
    #################################################################################################
    #################################################################################################
    #print("Prueba...")
    #archivo = open("pokes_test_binariz.txt")
    archivo = open("pre-procesados/pokes_test_binariz.txt")
    contenido = archivo.readlines()

    #print("################Contenido:###############")
    X = contenido[3:3+int(contenido[1])]
    #[print(x) for x in contenido]
    #print("################Contenido 2:###############")
    X = [i.split("\t") for i in X]
    #[print(x) for x in X]
    #print("################Contenido 3:###############")
    X = [list(map(float, i)) for i in X]
    #[print(x) for x in X]
    for i,j in zip(vProblema,X):
        j.append(i)

    #print("##########################################")

    #Y = contenido[3+int(contenido[1]):]
    #Y = [i.split("\t") for i in Y]
    #Y = [list(map(float, i)) for i in Y]

    X = n.array(X)
    #Y = n.array(Y)

    #print("X:")
    #print(X)

    #print("Y:")
    #print(Y)

    casosCorrectos = 0


    #CLASE SALIDA1  SALIDA 2  SALIDA 3
    Clases = ["Roca", "Agua", "Fuego","Planta"]

    for i in range(X.shape[1]): #para cada uno de los casos/registros de prueba
        #print("Prueba del Caso ", i + 1)
        casoi = X[:,i]
        #print("Caso Analizado: ")
        #print(casoi)

        Ycasoi = W.dot(casoi)
        #print("Salidas Generadas: ")
        #print(Ycasoi)

        """print("Salidas Real: ")
        Yrealcasoi = Y[:,i]
        print(Yrealcasoi)"""

        IndexMaxYcasoi = list(Ycasoi).index(max(Ycasoi))
        #IndexMaxYrealcasoi = list(Yrealcasoi).index(max(Yrealcasoi))

        #if IndexMaxYcasoi == IndexMaxYrealcasoi:
         #   casosCorrectos +=1

        #print("Clase Asignada: ", Clases[IndexMaxYcasoi])
        #print("Clase Real: ", Clases[IndexMaxYrealcasoi])
        if int(i)==len(X[0])-1:
            clase=Clases[IndexMaxYcasoi]
            #print("#####################################")
        """print()

    print("Total de Casos Analizados: ", X.shape[1])
    print("Total de Casos Correctos: ", casosCorrectos)

    print("Eficiencia del Asociador Lineal: ", casosCorrectos/X.shape[1]*100.0)"""
    print("Clase: ",clase)
    return clase

if __name__ == "__main__":
    respuesta= lineal([10,40,15,80,80])
    print(respuesta)
