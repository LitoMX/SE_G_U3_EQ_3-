import puntoZ as puntoZ
import iqr as iqr
import AsociadorLineal as lineal
import knnMain as knn
import discretizar as disc
import separar as sep
import id3Main as id3
import naiveBayes as bayes
import sys
import serial as conecta
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "main.ui"  # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Área de los Signals
        self.btn_conectar.clicked.connect(self.conectar)
        self.btn_generar.clicked.connect(self.generar)
        self.rad_promedio.clicked.connect(self.comando)
        self.rad_mediana.clicked.connect(self.comando)
        self.rad_maximo.clicked.connect(self.comando)
        self.rad_minimo.clicked.connect(self.comando)
        self.rad_moda.clicked.connect(self.comando)
        self.rad_1.clicked.connect(self.comando)
        self.rad_10.clicked.connect(self.comando)
        self.rad_30.clicked.connect(self.comando)
        self.rad_50.clicked.connect(self.comando)
        self.rad_100.clicked.connect(self.comando)
        self.arduino = None
        self.comand="p+001+030+f"
        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.control)
        self.vProblema = ""
        self.comandos = {
            "promedio": "001",
            "mediana": "002",
            "maximo": "003",
            "minimo": "004",
            "moda": "005",
            "1": "001",
            "10": "010",
            "30": "030",
            "50": "050",
            "100": "100"
        }

    # Área de los Slots

    def generar(self):
        self.segundoPlano.start(100)

    def conectar(self):
        try:
            if self.btn_conectar.text()=="Conectar":
                # puerto = self.txt_puerto.text()
                puerto = "COM3"  ###################################ajustar puerto
                self.arduino = conecta.Serial(puerto, baudrate=9600, timeout=1)
                self.btn_conectar.setText("Desconectar")
            elif self.btn_conectar.text()=="Desconectar":
                self.detener()
                self.btn_conectar.setText("Conectar")

        except Exception as error:
            print(error)

    def detener(self):
        self.segundoPlano.stop()
        self.arduino.close()

    def control(self):
        try:
            #print("comienza")
            if self.btn_conectar.text()=="Desconectar":
                print("generando muestra...")
                self.setWindowTitle("Generando muestra")
                self.txt_vProblema.setText("Generando...")
                self.txt_clasificacion.setText("")
                #comando = self.comando()
                print(self.comand)
                self.arduino.write(self.comand.encode())
                while self.arduino.read() == '':
                    pass  # Continúa esperando mientras arduino no termine calcular el vector problema

                self.vProblema = self.arduino.readline().decode()
                self.vProblema = self.vProblema.replace("\r", "")
                self.vProblema = self.vProblema.replace("\n", "")
                print(self.vProblema)

                if self.vProblema != "":
                    if self.vProblema[0]=="r" and self.vProblema[-1]=="f":
                        self.txt_vProblema.setText(self.vProblema[2:-2])
                        #print(self.vProblema[2:-2])
                        vProbl = self.vProblema[2:-2].split(",")
                        self.vProblema = []
                        for i in vProbl:
                            self.vProblema.append(int(i))
                        print("vector Problema: ", self.vProblema)
                        self.setWindowTitle("Muestra generada")
                        self.txt_clasificacion.setText("Clasificando...")
                        #self.detener()
                        outlier = None
                        titulo = ""
                        respuesta = "p+"
                        if self.vProblema != "":
                            self.setWindowTitle("Verificando Outliers...")
                            print("Verificando Outliers...")
                            if self.rad_iqr.isChecked():
                                outlier = iqr.iqr(self.vProblema)
                                if outlier[0] and outlier[1]:
                                    respuesta += "002"
                                    print("Outlier extremo, no procede")
                                    titulo = "Outlier Extremo"
                                    self.txt_clasificacion.setText("Outlier extremo")
                                elif outlier[0]:
                                    print("Outlier leve, no procede")
                                    respuesta += "001"
                                    titulo = "Outlier leve"
                                    self.txt_clasificacion.setText("Outlier leve")
                                elif not outlier[0] and not outlier[1]:
                                    print("Sin outlier iqr")
                                    respuesta += "000+"
                            elif self.rad_pz.isChecked():
                                outlier = puntoZ.punto_Z(self.vProblema)
                                if outlier:
                                    print("Outlier punto Z, no procede")
                                    respuesta += "001"
                                    titulo = "Outlier"
                                    self.txt_clasificacion.setText(titulo)
                                else:
                                    respuesta += "000+"
                            if respuesta[2:-1] == "000":
                                print("Comienza la clasificacion...")
                                resp = ""
                                if self.rad_knn.isChecked():
                                    resp = knn.knn(self.vProblema)
                                elif self.rad_id3.isChecked():
                                    disc.main_discretizar(self.vProblema)
                                    sep.separar()
                                    resp = id3.id3()
                                elif self.rad_bayes.isChecked():
                                    disc.main_discretizar(self.vProblema)
                                    sep.separar()
                                    resp = bayes.bayes()
                                elif self.rad_lineal.isChecked():
                                    resp = lineal.lineal(self.vProblema)
                                self.txt_clasificacion.setText(resp)
                                titulo = resp
                                if len(resp) > 4:
                                    resp = resp[:4]
                                respuesta += resp
                            respuesta += "+f"
                            print(respuesta)
                            self.arduino.write(respuesta.encode())
                            self.setWindowTitle(titulo)
                            while self.arduino.read() == '':
                                pass

                else:
                    self.setWindowTitle("selecciona Tipo, Tamaño, Outliers y Clasificar...")
                    #self.detener()
            else:
                self.setWindowTitle("Primero realiza la conexion...")


        except Exception as error:
            print(error)

    def seleccionado(self):
        self.select=False
        for rad_btn in [self.rad_promedio, self.rad_mediana, self.rad_maximo, self.rad_minimo, self.rad_moda]:
            #print("def selecc")
            if rad_btn.isChecked():
                #print("entra seleccionado rad_btn_1")
                for rad_btn_2 in [self.rad_1, self.rad_10 ,self.rad_30, self.rad_50 , self.rad_100]:
                    if rad_btn_2.isChecked():
                        #print("entra seleccionado rad_btn_2")
                        for rad_btn_3 in [self.rad_iqr,self.rad_pz]:
                         #   print("entra seleccionado rad_btn_3")
                            if rad_btn_3.isChecked():
                                for rad_btn_4 in [self.rad_knn, self.rad_id3, self.rad_bayes, self.rad_lineal]:
                                    if rad_btn_4.isChecked():
                          #              print("entra seleccionado rad_btn_4")
                                        self.select = True
                                        break

    def comando(self):
        comando = "p"
        for rad_btn in [self.rad_promedio, self.rad_mediana, self.rad_maximo, self.rad_minimo, self.rad_moda,
                        self.rad_1, self.rad_10, self.rad_30, self.rad_50, self.rad_100]:
            if rad_btn.isChecked():
                comando += "+" + self.comandos[rad_btn.objectName()[4:]]
        comando += "+f"
        return comando



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
