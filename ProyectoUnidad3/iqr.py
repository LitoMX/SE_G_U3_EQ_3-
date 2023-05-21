import csv
import numpy as np


def iqr(vector_problema):

    with open('pre-procesados/pokes_train.csv', newline='') as csvfile:
        leido = csv.reader(csvfile, delimiter=',')
        lista = list(leido)
    datos=[]
    for r in lista:
        vv = []
        for v in r[:-1]:
            vv.append(int(v))
        datos.append(vv)
    """[print(x) for x in datos]
    print("-"*30)"""

    datos_ordenados = np.sort(datos, axis=0)
    #[print(x) for x in datos_ordenados]

    n = len(datos_ordenados)

    q1_idx = int(0.25 * n)
    q3_idx = int(0.75 * n)

    q1 = datos_ordenados[q1_idx, :]
    q3 = datos_ordenados[q3_idx, :]
    iqr = q3 - q1

    """print("-"*30)

    print("Q1:", q1)
    print("Q3:", q3)
    print("IQR:", iqr)

    print("-"*30)"""

    lim_inf_3 = q1 - 3 * iqr
    #print("Limites inferiores para outliers extremos de 3:", lim_inf_3)
    lim_sup_3 = q3 + 3 * iqr
    #print("Limites superiores para outliers extremos de 3:", lim_sup_3)

    lim_inf_1_5 = q1 - 1.5 * iqr
    #print("Limites inferiores para outliers de 1.5:", lim_inf_1_5)
    lim_sup_1_5 = q3 + 1.5 * iqr
    #print("Limites superiores para outliers de 1.5:", lim_sup_1_5)

    num_outliers_3 = 0
    num_outliers_1_5 = 0
    #outliers=[ 1.5 -- 3 ]
    outliers=[False, False]
    for vp, vl3, vu3, vl1_5, vu1_5 in zip(vector_problema, lim_inf_3, lim_sup_3, lim_inf_1_5, lim_sup_1_5):
        if vp < vl1_5 or vp > vu1_5:
            outliers[0] = True
            num_outliers_1_5 += 1
        if vp < vl3 or vp > vu3:
            outliers[1] = True
            num_outliers_3 += 1

    """print("-"*30)
    print("el vector problema es: ", vector_problema)
    print("-"*30)"""

    """if outliers[0]:
        print("El vector problema es un outlier extremo de 3 según el método del IQR")
    else:
        print("El vector problema no es un outlier extremo de 3 según el método del IQR")

    if outliers[1]:
        print("El vector problema es un outlier de 1.5 según el método del IQR")
    else:
        print("El vector problema no es un outlier de 1.5 según el método del IQR")"""
    return outliers

if __name__ == "__main__":
    vp=np.array([80, 40, 100, 10, 1])
    respuesta = iqr(vp)
    print(respuesta)