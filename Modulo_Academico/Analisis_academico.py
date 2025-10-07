import pandas as pd
from generar_csvs import notas, matriculas, grupos

from generar_csvs import materias

#Cargar archivos CSV
notas = pd.read_csv("data/notas.csv")
materias = pd.read_csv("data/materias.csv")
matriculas = pd.read_csv("data/matriculas.csv")
grupos = pd.read_csv("data/grupos.csv")

print("===========================")
print("📊HUPA1: Promedio por grupo")
print("===========================")
#Debo relacionar tabla de notas con grupo pero es necesario usar la tabla materias como intermediaria
#Se crea un nuevo data frame usando un merge de ambas tablas
notas_con_grupo = pd.merge(notas, matriculas, on=["estudiante_id","materia_id"], how="left")
#El resultado vuelve y se fusiona con la tabla grupo
notas_con_grupo = pd.merge(notas_con_grupo, grupos [["id","nombre"]], left_on="grupo_id", right_on="id", how="left")
#Es inportante cambiar en nombre de la columna "nombre" pues hay muchos asi
notas_con_grupo = notas_con_grupo.rename(columns={"nombre": "grupo_nombre"})
#Sacamos el promedio ya con nombre de grupo y nota que ya estan en el DF notas_con_grupo
promedio_por_grupo = notas_con_grupo.groupby("grupo_nombre")["valor"].mean().sort_values(ascending=False)
print(promedio_por_grupo.round(2))

print("===========================")
print("📊HUPA2: Índice de reprobación por materia")
print("===========================")
#Se crea un dataframe nuevo filtrando en notas los resultados de menos de 3
notas_reprobadas = notas[notas["valor"]<3]
#El indice de reprobacion se busca dividiendo la cantidad de reprobadas por la cantidad total de notas x 100 para dar porcentaje
#Se debe entonces crear una tabla nueva aplicando contadores
#contador de notas por materia
total_notas_por_materia = notas.groupby("materia_id")["id"].count().reset_index(name="total")
#Contar reprobadas por materia
reprobadas_por_materia = notas_reprobadas.groupby("materia_id")["id"].count().reset_index(name="reprobadas")
#Unir ambas DF de conteo
reprobacion = pd.merge(total_notas_por_materia, reprobadas_por_materia, on="materia_id", how="left")
#Rellenar con cero valores nulos por si alguna materia no tiene reprobados
reprobacion["reprobadas"] = reprobacion["reprobadas"].fillna(0)
#Formula para Calcurar porcentaje de reprobacion
reprobacion["% reprobación"] = (reprobacion["reprobadas"] / reprobacion["total"]) * 100
#Unir este data frame con la tabla materia para relacionar el Id con el nombre
reprobacion = pd.merge(reprobacion, materias[["id", "nombre"]], left_on="materia_id", right_on="id", how="left")
#Seleccionar columnas y ordenar
reprobacion = reprobacion[["nombre", "% reprobación"]].sort_values(by="% reprobación", ascending=False)
#Mostrar resultados
print("\n📉 Materias con mayor índice de reprobación:")
print(reprobacion.round(2))
