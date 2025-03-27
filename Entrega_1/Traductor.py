# Nombre del Programa: Traductor para sordos                                      #
# Autor: Guillermo Cardenas, Juan Suarez                                          #
# Versión: 3.4.15                                                                 #
# Descripción: Algoritmo de traduccion de lenguaje de señas (Agente Inteligente)  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#Importamos os para limpiar la pantalla
import os

# Definir el alfabeto de lenguaje de señas (27 letras)
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "[:27]

# Función para mostrar el menú interactivo
def mostrar_menu():
    os.system('cls')  # Limpiar la pantalla
    print("=== Lenguaje de Señas a Texto ===")
    print("Selecciona una letra (0 para salir):")
    for i, letra in enumerate(alfabeto):
        print(f"{i + 1}. {letra}")
    print("=========================")

# Función para almacenar las letras seleccionadas
def traducir_señas():
    palabra = ""
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == 0:
                break
            elif 1 <= opcion <= len(alfabeto):
                letra_seleccionada = alfabeto[opcion - 1]
                palabra += letra_seleccionada
                print(f"Letra seleccionada: {letra_seleccionada}")
                print(f"Palabra actual: {palabra}")
            else:
                print("Opción inválida. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")
        input("Presiona Enter para continuar...")

    print(f"Palabra final: {palabra}")

# Ejecutar el programa
traducir_señas()
