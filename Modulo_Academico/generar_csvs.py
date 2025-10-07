import pandas as pd
import numpy as np
import random
from faker import Faker
import os

fake = Faker('es_CO')
random.seed(42)
np.random.seed(42)

# Crear carpeta de salida
os.makedirs("data", exist_ok=True)

# Programas
programas = ["Desarrollo de Software", "Soporte Técnico"]
grupos_por_programa = ["Grupo A", "Grupo B"]

# Roles
roles = ["estudiante", "docente"]

# Semestre y periodo
semestre = 1
periodo = "Marzo-Junio 2026"

# Fechas fijas para las notas
fechas_notas = ["2026-04-12", "2026-05-24", "2026-07-05"]

# ID contadores
id_usuario = 1
id_estudiante = 1
id_docente = 1
id_materia = 1
id_grupo = 1
id_matricula = 1
id_nota = 1

usuarios = []
estudiantes = []
docentes = []
materias = []
grupos = []
matriculas = []
notas = []

# Crear docentes y materias
docentes_por_programa = {}

for programa in programas:
    docentes_ids = []
    for i in range(4):  # 4 docentes por programa
        nombre = fake.name()
        correo = fake.email()
        usuarios.append({
            "id": id_usuario,
            "nombre": nombre,
            "correo": correo,
            "contraseña": "1234",
            "rol": "docente",
            "estado": "activo"
        })

        docentes.append({
            "usuario_id": id_usuario,
            "especialidad": random.choice(["Bases de Datos", "Redes", "Desarrollo Web"]),
            "nivelAcademico": random.choice(["Especialista", "Magíster"]),
            "departamento": programa
        })

        docentes_ids.append(id_usuario)
        id_usuario += 1
        id_docente += 1

    docentes_por_programa[programa] = docentes_ids

# Crear materias y grupos
materias_por_programa = {}

horas_disponibles = [
    "lunes 8am", "lunes 10am", "martes 8am", "martes 10am",
    "miércoles 8am", "miércoles 10am", "jueves 8am", "jueves 10am"
]

materias_base = ["Frontend", "Backend", "Base de Datos", "Lógica de Programación"]

for programa in programas:
    materias_ids = []
    horario_idx = 0
    for i in range(4):  # 4 materias por programa
        docente_id = random.choice(docentes_por_programa[programa])
        nombre = f"{materias_base[i]} - {horas_disponibles[horario_idx]}"
        codigo = f"{programa[:2].upper()}-{i+1:03d}"

        materias.append({
            "id": id_materia,
            "nombre": nombre,
            "codigo": codigo,
            "docente_id": docente_id
        })
        materias_ids.append(id_materia)

        # Crear 2 grupos por materia
        for grupo_nombre in grupos_por_programa:
            grupos.append({
                "id": id_grupo,
                "nombre": f"{grupo_nombre} - {programa}",
                "materia_id": id_materia,
                "semestre": semestre
            })
            id_grupo += 1

        id_materia += 1
        horario_idx += 1

    materias_por_programa[programa] = materias_ids

# Crear estudiantes y matrículas
for programa in programas:
    for grupo_nombre in grupos_por_programa:
        for i in range(30):  # 30 estudiantes por grupo
            nombre = fake.name()
            correo = fake.email()

            usuarios.append({
                "id": id_usuario,
                "nombre": nombre,
                "correo": correo,
                "contraseña": "1234",
                "rol": "estudiante",
                "estado": "activo"
            })

            estudiantes.append({
                "usuario_id": id_usuario,
                "programa": programa,
                "semestre": semestre
            })

            estudiante_id = id_usuario
            id_usuario += 1
            id_estudiante += 1

            # Matricular a las 4 materias del programa
            for materia_id in materias_por_programa[programa]:
                # Encontrar grupo correspondiente
                grupo_id = next(g["id"] for g in grupos if g["materia_id"] == materia_id and grupo_nombre in g["nombre"])

                matriculas.append({
                    "id": id_matricula,
                    "estudiante_id": estudiante_id,
                    "materia_id": materia_id,
                    "grupo_id": grupo_id,
                    "periodo": periodo
                })

                # 3 notas por estudiante por materia
                for fecha in fechas_notas:
                    valor = round(np.random.normal(3.5, 0.8), 1)
                    valor = max(0, min(valor, 5))  # Limitar entre 0 y 5

                    notas.append({
                        "id": id_nota,
                        "valor": valor,
                        "tipoEvaluacion": random.choice(["Parcial", "Taller", "Final"]),
                        "fecha": fecha,
                        "estudiante_id": estudiante_id,
                        "materia_id": materia_id
                    })
                    id_nota += 1

                id_matricula += 1

# Guardar CSVs
pd.DataFrame(usuarios).to_csv("data/usuarios.csv", index=False)
pd.DataFrame(estudiantes).to_csv("data/estudiantes.csv", index=False)
pd.DataFrame(docentes).to_csv("data/docentes.csv", index=False)
pd.DataFrame(materias).to_csv("data/materias.csv", index=False)
pd.DataFrame(grupos).to_csv("data/grupos.csv", index=False)
pd.DataFrame(matriculas).to_csv("data/matriculas.csv", index=False)
pd.DataFrame(notas).to_csv("data/notas.csv", index=False)

print("✅ Archivos CSV generados en la carpeta 'data/'")