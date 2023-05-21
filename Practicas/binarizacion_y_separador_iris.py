import csv
import random as rnd
clase_binario = {'Iris-setosa': [0, 0, 1],
               'Iris-versicolor': [0, 1, 0],
               'Iris-virginica': [1, 0, 0]}


def binarizar():
    terminado = "Archivos no guardados correctamente"
    try:
        binarizado=[]
        with open('originales\datosiris.csv', newline='') as csvfile:
            leido = csv.reader(csvfile, delimiter=',')
            for renglon in leido:
                valor = clase_binario[renglon[-1]]
                r=[]
                for x in renglon[:-1]:
                    r.append(x)
                for x in valor:
                    r.append(x)
                binarizado.append(r)

        cant_datos = len(binarizado)
        cant_binarios = len(clase_binario['Iris-virginica'])
        cant_atributos = len(binarizado[0])-cant_binarios

        train = int(len(binarizado) * .7)
        test = len(binarizado) - train

        print(cant_datos, train, test)


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

        with open('pre-procesados\iris_completo_binarizado.txt', 'w') as f:
            f.write(str(cant_datos) + '\n')
            f.write(str(cant_atributos) + '\n')
            f.write(str(cant_binarios) + '\n')
            for item in binarizado:
                line = '\t'.join(map(str, item)) + '\n'
                f.write(line)

        with open('pre-procesados\iris_train_binariz.txt', 'w') as f:
            f.write(str(len(m_train[0])) + '\n')
            f.write(str(cant_atributos) + '\n')
            f.write(str(cant_binarios) + '\n')
            for item in m_train:
                line = '\t'.join(map(str, item)) + '\n'
                f.write(line)

        with open('pre-procesados\iris_test_binariz.txt', 'w') as f:
            f.write(str(len(m_test[0])) + '\n')
            f.write(str(cant_atributos) + '\n')
            f.write(str(cant_binarios) + '\n')
            for item in m_test:
                line = '\t'.join(map(str, item)) + '\n'
                f.write(line)

        terminado = "Archivos guardados correctamente"
    except Exception as ex:
        print(ex)
    return terminado


print(binarizar())
