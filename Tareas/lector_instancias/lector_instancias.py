import csv
import sys
import random as rnd
import numpy as np
import pandas as p
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "lector_instancias.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals
        self.btn_crear.clicked.connect(self.crear)

    # Área de los Slots
    def crear(self):
        nombre=self.txt_nombre.text()
        total=self.txt_total.text()
        train = self.txt_train.text()


        if not nombre == "" and not total == "" and not train == "":
            nombre+=".csv"

            try:
                total = int(total)
                train = int(train)
                if total > train:
                    registros = p.read_csv(nombre, sep=',')

                    test = total - train

                    matriz = np.array(registros).reshape(len(registros), len(registros.columns))

                    print("matriz:")
                    [print(i) for i in matriz]

                    matriz_train = [[0] * (len(matriz[0])) for i in range(train)]
                    matriz_test = [[0] * (len(matriz[0])) for i in range(test)]
                    print(len(matriz))
                    indices = rnd.sample(range(0, len(matriz)), total)


                    for i in range(train):
                        for j in range(len(matriz[0])):
                            matriz_train[i][j] = matriz[indices[i]][j]

                    for i in range(test):
                        for j in range(len(matriz[0])):
                            matriz_test[i][j] = matriz[indices[i+test]][j]

                    print("indices:")
                    print(indices)
                    print("matriz_train:")
                    [print(i) for i in matriz_train]
                    print("matriz_test:")
                    [print(i) for i in matriz_test]

                    with open('train.csv', 'w', newline='') as file:
                        wr = csv.writer(file, delimiter=',')
                        wr.writerows(matriz_train)

                    with open('test.csv', 'w', newline='') as file:
                        wr = csv.writer(file, delimiter=',')
                        wr.writerows(matriz_test)

                    print("Archivos creados satisfactoriamente")

                else:
                    print("total debe ser mayor a test")

            except Exception as exeption:
                print(exeption)


        else:
            print("llena todos los campos")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())