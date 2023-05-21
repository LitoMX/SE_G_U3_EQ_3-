import csv
import numpy as np

def punto_Z(vector_problema):

    print("comienza punto z")
    with open('pre-procesados/pokes_train.csv', newline='') as csvfile:
        leido = csv.reader(csvfile, delimiter=',')
        lista = list(leido)
    # Extraer los valores numéricos de los datos de entrenamiento

    datos=[]
    for r in lista:
        vv=[]
        for v in r[:-1]:
            vv.append(float(v))
        datos.append(vv)

    media = np.mean(datos, axis=0)
    print("Media: ",media)
    print("-" * 30)
    desv_est = np.std(datos, axis=0)
    print("Desviacion estandar: ",desv_est)
    print("-" * 30)
    #print(vector_problema)

    # Definir los límites para los puntajes Z considerados outliers
    limite_pz = 3
    pz=[]
    """for v,m,d in zip(vector_problema,media, desv_est):
        print("entro zip")
        pz.append((v-float(m)/float(d)))
    print("puntosZ: ",pz)"""

    pz = (vector_problema - media) / desv_est
    # Verificar si el vector problema contiene outliers
    outliers =False
    for p in pz:
        if np.abs(p) > limite_pz:
            outliers=True
            break

    """print("limite punto Z: ",limite_pz)
    print("-" * 30)
    print("puntos Z: ",pz)
    print("-" * 30)
    if outliers:
        print("El vector problema es un outlier.")
    else:
        print("El vector problema no es un outlier.")
    print("-" * 30)"""
    return outliers

if __name__ == "__main__":
    vp=np.array([80, 40, 100, 10, 1])
    respuesta = punto_Z(vp)
    print(respuesta)