import pandas as pd
def leerArchivo(archivo):
    matriz = pd.read_excel(archivo, sheet_name= 'Hoja1')
    ataque = list(matriz["Ataque"])
    defensa = list(matriz["Defensa"])
    atqesp = list(matriz["AtqEsp"])
    defesp = list(matriz["DefEsp"])
    vel = list(matriz["Velocidad"])
    m = {'ataque':ataque,'defensa':defensa,'atqesp':atqesp,'defesp':defesp,'vel':vel}
    return m

def valor_min(m):
    val_min = []
    for i in list(m.keys()):
        val_min.append(min(m[i]))
    return val_min
def valor_max(m):
    val_max = []
    for i in list(m.keys()):
        val_max.append(max(m[i]))
    return val_max
def m(valores_minimos, valores_maximos):
    val_m = []
    for i in range(len(valores_maximos)):
        val_m.append((1-0)/(valores_maximos[i]-valores_minimos[i]))
    return val_m
def b(valores_m, valores_maximos):
    val_b = []
    for i in range(len(valores_maximos)):
        val_b.append((1 - (valores_m[i] * valores_maximos[i])))
    return val_b
def normalizacion(valores_m, matriz, valores_b):
    tabla_norm = []
    cont = 0
    for i in list(matriz.keys()):
        for x in matriz[i]:
            tabla_norm.append(valores_m[cont]*x+valores_b[cont])
        cont += 1
    return tabla_norm

matriz = leerArchivo("pokes.xlsx")
print(matriz)

valores_minimos = valor_min(matriz)
print("Valores Minimos: ", valores_minimos)

valores_maximos = valor_max(matriz)
print("Valores Maximos", valores_maximos)

valores_m = m(valores_minimos, valores_maximos)
print("Valores m", valores_m)

valores_b = b(valores_m, valores_maximos)
print("Valores b", valores_b)

tabla_normalizada = normalizacion(valores_m, matriz, valores_b)

print("----TABLA NORMALIZADA----")
print(tabla_normalizada)
