import csv


def leerArchivo():
    atributos = []
    clase = []
    with open('originales/pokes.csv', newline='') as csvfile:
        leido = csv.reader(csvfile, delimiter=',')
        for row in leido:
            clase.append(row[-1])
            row = row[:-1]
            atributos.append([float(x) for x in row])
    return clase, atributos


def intervalos(atributos, num_intervalos):
    intervalos = []
    for i in range(len(atributos[0])):
        valoresXColumnas = [row[i] for row in atributos]
        valMin = min(valoresXColumnas)
        valMax = max(valoresXColumnas)
        tamIntervalo = (valMax - valMin) / num_intervalos
        intervalos.append([valMin + tamIntervalo * i for i in range(num_intervalos)])
    return intervalos


def discretizar(atributos, num_intervalos, intervalos):
    atributos_discretizados = []
    for row in atributos:
        renglon_discretizado = []
        for i in range(len(row)):
            for j in range(num_intervalos):
                if row[i] <= intervalos[i][j]:
                    renglon_discretizado.append(j + 1)
                    break
                elif j == num_intervalos - 1:
                    renglon_discretizado.append(j + 1)
                    break
        atributos_discretizados.append(renglon_discretizado)
    return atributos_discretizados


def guardarCSV(discretizado,nomyclase):
    with open('pre-procesados/pokes_discretizado.csv', 'w', newline='') as archivo:
        writer = csv.writer(archivo, delimiter=',')
        #writer.writerow(cab)
        for n, d in zip(nomyclase, discretizado):
            writer.writerow([d[0], d[1], d[2], d[3], d[4],n])


clas, arch = leerArchivo()
inter = intervalos(arch, 5)
discre = discretizar(arch, 5, inter)
guardarCSV(discre, clas)
