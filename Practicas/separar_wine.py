import csv
import random as rnd

with open('pre-procesados/wine_discretizado.csv', newline='') as csvfile:
    leido = csv.reader(csvfile, delimiter=',')
    lista = list(leido)

    print(len(lista))

    train = int(len(lista) * .7)
    test = len(lista) - train


    m_train = [[0] * (len(lista[0])) for i in range(train)]
    m_test = [[0] * (len(lista[0])) for i in range(test)]

    indices = rnd.sample(range(0, len(lista)), len(lista))

    for i in range(train):
        for j in range(len(lista[0])):
            m_train[i][j] = lista[indices[i]][j]

    for i in range(test):
        for j in range(len(lista[0])):
            m_test[i][j] = lista[indices[i + test]][j]

with open('pre-procesados/wine_discret_train.csv', 'w', newline='') as csvfile:
    write = csv.writer(csvfile, delimiter=',')
    for fila in m_train:
        write.writerow(fila)

with open('pre-procesados/wine_discret_test.csv', 'w', newline='') as csvfile:
    write = csv.writer(csvfile, delimiter=',')
    for fila in m_test:
        write.writerow(fila)
