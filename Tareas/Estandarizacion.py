import pandas as pd
import statistics
def leerArchivo(archivo):
    matriz = pd.read_excel(archivo, sheet_name= 'Hoja1')
    ataque = list(matriz["Ataque"])
    defensa = list(matriz["Defensa"])
    atqesp = list(matriz["AtqEsp"])
    defesp = list(matriz["DefEsp"])
    vel = list(matriz["Velocidad"])
    m = {'ataque':ataque,'defensa':defensa,'atqesp':atqesp,'defesp':defesp,'vel':vel}
    return m

def promedios(m):
    lpromedios = []
    for i in m:
        lpromedios.append(statistics.mean(m[i]))
    return lpromedios

def desestandar(m):
    ldesvestandar = []
    for i in m:
        ldesvestandar.append(statistics.pstdev(m[i]))
    return ldesvestandar

def estandarizacion(m,lprom,ldesv):
    matriz = []
    cont = 0
    a = []
    for i in m:
        a.clear()
        for j in range(len(m[i])):
            a.append((m[i][j]-lprom[cont])/ldesv[cont])
        matriz.append(a)
        cont += 1
    return matriz



matriz = leerArchivo("../Archivos/pokes.xlsx")
print(matriz)
lpromedios = promedios(matriz)
print(lpromedios)
ldesvestandar = desestandar(matriz)
print(ldesvestandar)
nmatriz = estandarizacion(matriz,lpromedios,ldesvestandar)
print(nmatriz)