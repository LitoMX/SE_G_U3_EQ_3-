import csv
import random as rnd
def separar():
    with open('pre-procesados/pokes_discretizado_proyectoU3.csv', newline='') as csvfile:
        leido = csv.reader(csvfile, delimiter=',')
        leid = list(leido)
        lista = leid[:-1]

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

        m_test.append(leid[-1])

    with open('pre-procesados/pokes_discret_train_proyectoU3.csv', 'w', newline='') as csvfile:
        write = csv.writer(csvfile, delimiter=',')
        for fila in m_train:
            write.writerow(fila)
    
    with open('pre-procesados/pokes_discret_test_proyectoU3.csv', 'w', newline='') as csvfile:
        write = csv.writer(csvfile, delimiter=',')
        #for fila in m_test:
        write.writerow(leid[-1])


if __name__ == "__main__":
    separar()