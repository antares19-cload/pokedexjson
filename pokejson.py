import os
import json
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

# Guardar la información del Pokémon en el directorio del repositorio
POKEDEX_DIR = "pokedexjson"

# Asegúrate de que el directorio exista (se crea si no existe)
os.makedirs(POKEDEX_DIR, exist_ok=True)

def guardar_en_json(pokemon_info):
    # Crear el nombre del archivo JSON basado en el nombre del Pokémon
    nombre_archivo = f"{POKEDEX_DIR}/{pokemon_info['name']}.json"
    
    # Guardar la información del Pokémon en un archivo JSON
    with open(nombre_archivo, "w") as f:
        json.dump(pokemon_info, f, indent=4)
    
    # Confirmar que la información ha sido guardada
    print(f"Información guardada en {nombre_archivo}")

# Función para obtener información del Pokémon de la API
def obtener_info_pokemon(pokemon_nombre):
    # Hacer una solicitud a la API de Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_nombre.lower()}"
    response = requests.get(url)
    
    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        pokemon_info = response.json()
        guardar_en_json(pokemon_info)  # Guardar la información en JSON
        return pokemon_info
    else:
        print("Pokémon no encontrado.")
        return None

# Función para mostrar la imagen del Pokémon en una ventana
def mostrar_imagen(pokemon_info):
    img_url = pokemon_info['sprites']['front_default']  # URL de la imagen
    img_response = requests.get(img_url)
    img_data = Image.open(BytesIO(img_response.content))

    # Crear una ventana de tkinter para mostrar la imagen
    ventana = tk.Tk()
    ventana.title(pokemon_info['name'])
    
    img_tk = ImageTk.PhotoImage(img_data)  # Convertir la imagen a formato Tkinter
    label = tk.Label(ventana, image=img_tk)
    label.pack()
    
    ventana.mainloop()  # Mostrar la ventana

# Función principal para la interfaz de usuario
def main():
    pokemon_nombre = input("Ingrese el nombre del Pokémon: ")  # Pedir el nombre del Pokémon
    pokemon_info = obtener_info_pokemon(pokemon_nombre)  # Obtener información del Pokémon
    
    if pokemon_info:
        # Mostrar información básica del Pokémon
        print(f"ID: {pokemon_info['id']}, Nombre: {pokemon_info['name']}, Tipos: {[t['type']['name'] for t in pokemon_info['types']]}")
        mostrar_imagen(pokemon_info)  # Mostrar la imagen del Pokémon

# Ejecutar la función principal si el script es ejecutado
if __name__ == "__main__":
    main()
