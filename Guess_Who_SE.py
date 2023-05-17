import mysql.connector
import random

# Conectar a la base de datos
conexion = mysql.connector.connect(
  host="localhost",
  user="root",
  password="TypeRFD6.",
  database="basededatos"
)

cursor = conexion.cursor()

# Verificar que hay preguntas y conocimientos en las tablas correspondientes
cursor.execute('SELECT COUNT(*) FROM preguntas')
num_preguntas = cursor.fetchone()[0]
if num_preguntas == 0:
    print("No hay preguntas en la tabla 'preguntas'.")
    exit()

cursor.execute('SELECT COUNT(*) FROM conocimientos')
num_conocimientos = cursor.fetchone()[0]
if num_conocimientos == 0:
    print("No hay conocimientos en la tabla 'conocimientos'.")
    exit()

# Obtener las preguntas de la tabla correspondiente
cursor.execute('SELECT pregunta FROM preguntas')
preguntas = [pregunta[0] for pregunta in cursor.fetchall()]

# Obtener los conocimientos de la tabla correspondiente
cursor.execute('SELECT jugador, conocimiento FROM conocimientos')
base_conocimientos = {}
for jugador, conocimiento in cursor.fetchall():
    if jugador not in base_conocimientos:
        base_conocimientos[jugador] = []
    base_conocimientos[jugador].append(conocimiento)



# Obtener las preguntas de la tabla correspondiente
cursor.execute('SELECT pregunta FROM preguntas')
preguntas = [pregunta[0] for pregunta in cursor.fetchall()]

# Obtener los conocimientos de la tabla correspondiente
cursor.execute('SELECT deporte, conocimiento FROM conocimientos')
base_conocimientos = {}
for jugador, conocimiento in cursor.fetchall():
    if jugador not in base_conocimientos:
        base_conocimientos[jugador] = []
    base_conocimientos[jugador].append(conocimiento)

# Mostrar opciones de jugadores disponibles
print("Jugadores disponibles:")
for i, jugador in enumerate(base_conocimientos.keys()):
    print(f"{i+1}. {jugador}")

# Leer opción elegida por el usuario
opcion = input("Elije el jugador que deseas adivinar (ingresa el numero correspondiente): \n")
while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(base_conocimientos):
    opcion = input("Opcion invalida. Elije el jugador que deseas adivinar (ingresa el numero correspondiente):\n ")
# Obtener el jugador correspondiente a la opción elegida
jugador_disponibles = list(base_conocimientos.keys())
jugador_elegido = jugador_disponibles[int(opcion)-1]

# Realizar las preguntas al usuario
respuestas = {}
for pregunta in preguntas:
    respuesta = input(f"\n{pregunta}: ")
    respuestas[pregunta] = respuesta.lower()



# Comprobar si las respuestas son correctas
encontrado = False
for jugador, conocimientos in base_conocimientos.items():
    es_el_jugador = True
    for conocimiento in conocimientos:
        if ":" not in conocimiento:
            continue
        pregunta, respuesta_correcta = conocimiento.split(":")
        respuesta_usuario = respuestas.get(pregunta.lower(), "").strip()
        if respuesta_usuario != respuesta_correcta.lower():
            es_el_jugador = False
            break
    if es_el_jugador:
        encontrado = True
        if jugador == jugador_elegido:
            print(f"\nFelicidades, has adivinado el deporte!\nJUGADOR: {jugador}\n")
        else:
            print(f"Lo siento, no adivinaste")
        break

    if encontrado:
        break

if not encontrado:
    print("Lo siento, tus respuestas no indican ningun jugador de la base de conocimientos.")