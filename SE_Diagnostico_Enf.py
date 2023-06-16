import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('enfermedades.db')
cursor = conn.cursor()

# Función para realizar la encuesta médica
def realizar_encuesta():
    sintomas_seleccionados = []

    # Pregunta por los síntomas disponibles
    cursor.execute("SELECT nombre FROM Sintomas")
    sintomas_disponibles = cursor.fetchall()

    # Preguntar por cada síntoma
    for sintoma in sintomas_disponibles:
        pregunta = f"¿Tiene {sintoma[0]}? (s/n): "
        respuesta = input(pregunta)
        
        while respuesta.lower() not in ['s', 'n']:
            print("Por favor, responda 's' para sí o 'n' para no.")
            respuesta = input(pregunta)
        
        if respuesta.lower() == 's':
            sintomas_seleccionados.append(sintoma[0])

    # Realizar inferencias
    enfermedades_inferidas = []
    for enfermedad, condiciones in obtener_reglas():
        if all(condicion in sintomas_seleccionados for condicion in condiciones):
            enfermedades_inferidas.append(enfermedad)

    # Imprimir resultados
    if enfermedades_inferidas:
        print("Las enfermedades que podrías tener son:")
        for enfermedad in enfermedades_inferidas:
            print(enfermedad)
    else:
        print("No se encontraron enfermedades coincidentes.")

# Función para obtener las reglas desde la base de datos
def obtener_reglas():
    cursor.execute("SELECT enfermedad_id, GROUP_CONCAT(s.nombre) FROM Enfermedades_Sintomas es \
                    JOIN Sintomas s ON es.sintoma_id = s.id \
                    GROUP BY enfermedad_id")
    reglas = cursor.fetchall()
    reglas_formateadas = []

    for regla in reglas:
        enfermedad_id = regla[0]
        sintomas = regla[1].split(',')
        reglas_formateadas.append((obtener_nombre_enfermedad(enfermedad_id), sintomas))

    return reglas_formateadas

# Función para obtener el nombre de la enfermedad
def obtener_nombre_enfermedad(enfermedad_id):
    cursor.execute("SELECT nombre FROM Enfermedades WHERE id = ?", (enfermedad_id,))
    nombre = cursor.fetchone()[0]
    return nombre

# Ejecutar la encuesta médica
realizar_encuesta()

# Cerrar la conexión a la base de datos
conn.close()
