import csv
import random as rnd
clase_binario = {'Planta': [0, 0, 0, 1],
               'Fuego': [0,0,1,0],
               'Agua': [0,1,0,0],
               'Roca': [1,0,0,0]}


def binarizar():
    terminado = "Archivos no guardados correctamente"
    try:
        binarizado=[]
        with open('originales/pokes.csv', newline='') as csvfile:
            leido = csv.reader(csvfile, delimiter=',')
            for i,renglon in enumerate(leido):
                if i==0:
                    continue
                valor = clase_binario[renglon[-1]]
                r=[]
                for x in renglon[:-1]:
                    r.append(x)
                for x in valor:
                    r.append(x)
                binarizado.append(r)
        cant_datos = len(binarizado)
        cant_binarios = len(clase_binario['Planta'])
        cant_atributos = len(binarizado[0])-cant_binarios

        train = int(len(binarizado) * .7)
        test = len(binarizado) - train

        m_train = [[0] * (len(binarizado[0])) for i in range(train)]
        m_test = [[0] * (len(binarizado[0])) for i in range(test)]

        indices = rnd.sample(range(0, len(binarizado)), cant_datos)

        for i in range(train):
            for j in range(len(binarizado[0])):
                m_train[i][j] = binarizado[indices[i]][j]

        for i in range(test):
            for j in range(len(binarizado[0])):
                m_test[i][j] = binarizado[indices[i + test]][j]


        binarizado = list(map(list, zip(*binarizado)))
        m_train = list(map(list, zip(*m_train)))
        m_test = list(map(list, zip(*m_test)))


        with open('pre-procesados/pokes_binarizado.csv', 'w', newline='') as archivo:
            writer = csv.writer(archivo, delimiter=',')
            writer.writerow([cant_datos])
            writer.writerow([cant_atributos])
            writer.writerow([cant_binarios])
            writer.writerows(binarizado)

        with open('pre-procesados/pokes_train_binariz.csv', 'w', newline='') as archivo:
            writer = csv.writer(archivo, delimiter=',')
            writer.writerow([len(m_train[0])])
            writer.writerow([cant_atributos])
            writer.writerow([cant_binarios])
            writer.writerows(m_train)

        with open('pre-procesados/pokes_test_binariz.csv', 'w', newline='') as archivo:
            writer = csv.writer(archivo, delimiter=',')
            writer.writerow([len(m_test[0])])
            writer.writerow([cant_atributos])
            writer.writerow([cant_binarios])
            writer.writerows(m_test)

        terminado = "Archivos guardados correctamente"
    except Exception as exeption:
        print(exeption)
    return terminado


print(binarizar())
