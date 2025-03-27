# Nombre del Programa: Traductor para sordos                                      #
# Autor: Guillermo Cardenas, Juan Suarez  .                                       #
# Versión: 2.4.21                                                                 #
# Descripción: Algoritmo de traduccion de lenguaje de señas (Sistema de busquedas)#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os # Importa el módulo os para interactuar con el sistema de archivos
from PIL import Image # Importa la clase Image del módulo PIL para trabajar con imágenes
import matplotlib.pyplot as plt # Importa matplotlib para mostrar las imágenes
from collections import deque # Importa deque para realizar la búsqueda por anchura

# Ruta de la carpeta que contiene las imágenes
directorio_imagenes = r'C:\Users\aasal\OneDrive\Documentos\Universidad\Inteligencia artificial\Entrega 2\Abecedario'

# Función para realizar la búsqueda por anchura
def busqueda_anchura(letra):
    cola = deque([directorio_imagenes]) # Inicializa la cola con el directorio de imágenes
    
    while cola:
        directorio_actual = cola.popleft() # Obtiene y elimina el primer elemento de la cola
        for entrada in os.listdir(directorio_actual): # Itera sobre las entradas en el directorio actual
            ruta = os.path.join(directorio_actual, entrada)  # Construye la ruta completa de la entrada
            if os.path.isdir(ruta): # Si la entrada es un directorio, la añade a la cola
                cola.append(ruta)
            elif os.path.isfile(ruta) and entrada.lower().startswith(letra.lower()) and entrada.endswith('.jpg'):
                # Si la entrada es un archivo y el nombre del archivo empieza con la letra dada y termina con '.jpg'
                return Image.open(ruta) # Abre y retorna la imagen
    
    return None # Retorna None si no se encuentra la imagen

# Función para mostrar la imagen
def mostrar_imagen(imagen):
    if imagen is not None:
        plt.imshow(imagen)  # Muestra la imagen usando matplotlib
        plt.axis('off')  # Oculta los ejes
        plt.show()  # Muestra la ventana con la imagen
    else:
        print("Imagen no encontrada.")  # Imprime un mensaje si no se encuentra la imagen

# Función principal que gestiona la interacción con el usuario
def main():
    while True:
        letra = input("Introduce una letra del abecedario, presiona el punto (.) para salir : ").upper() # Solicita una letra al usuario
        if letra == '.':
            break # Si el usuario introduce '.', termina el programa
        elif len(letra) != 1 or not letra.isalpha():
            print("Por favor, introduce una sola letra válida.") # Verifica que la entrada sea una letra válida
            continue
        
        imagen = busqueda_anchura(letra) # Realiza la búsqueda de la imagen correspondiente a la letra
        mostrar_imagen(imagen) # Muestra la imagen encontrada

# Verifica si el script es ejecutado directamente y llama a la función principal
if __name__ == "__main__":
    main()


