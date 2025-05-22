import random

imagenes = [
    # Se definen varios ejemplos de propiedades extraídas de imágenes de la camara
    {"objeto": "silla", "categoria": "Mixta", "ubicacion": "Flanco inferior derecho", "esquivar": "Ve a la izquierda o sigue derecho con prudencia", "llegar": "Dirígete un poco a la derecha"},
    {"objeto": "Pelota", "categoria": "Obstáculo", "ubicacion": "Flanco inferior", "esquivar": "Rodéalo a la izquierda o a la derecha teniendo cuidado de no pisarla.", "llegar": "Sigue derecho con prudencia."},
    {"objeto": "Mesa", "categoria": "Mixta", "ubicacion": "Flanco izquierdo", "esquivar": "Ve a la derecha o sigue derecho con prudencia.", "llegar": "Sigue adelante dirigiéndote un poco a la izquierda"},
    {"objeto": "Cama", "categoria": "Mixta", "ubicacion": "Centro", "esquivar": "Dirígete a la izquierda o a la derecha.", "llegar": "Sigue adelante"},
    {"objeto": "Puerta", "categoria": "Interés", "ubicacion": "Centro", "esquivar": "Dirígete a la izquierda o a la derecha.", "llegar": "Sigue adelante"}
]

print("\nHola! Soy tu asistente visual personal. \n")

mode = input("Presione 1 si desea mi asistencia o 2 si no la necesita: \n\n")

def detectarImagen(img):
    #Simula la deteccion de objetos en un entorno al escoger al azar de una lista predefinida
    return random.choice(img) 
    
def analizar(entorno):
    analizar = 1 #Variable para poder detener el proceso de analisis de entorno

    while analizar == 1:
        print("Estoy analizando el entorno... \n")
        print("Por favor, espera un momento... \n")

        imagenDetectada = detectarImagen(entorno) #Guarda las propiedades de la imagen en una variable
        print("Estoy viendo un(a) " + imagenDetectada["objeto"] + " en " + imagenDetectada["ubicacion"])

        if imagenDetectada["categoria"] == "Mixta":
            print("Podrías necesitar usarlo(a). Si es así, por favor " + imagenDetectada["llegar"] + ". De lo contrario, " + imagenDetectada["esquivar"])
        elif imagenDetectada["categoria"] == "Obstáculo":
            print("Por favor " + imagenDetectada["esquivar"])
        elif imagenDetectada["categoria"] == "Interés":
            print("Para dirigirte hacia el objeto, por favor " + imagenDetectada["llegar"])

        continuar = input("¿Deseas continuar analizando el entorno? (1 para continuar, 2 para detener): \n")
        # Se le pregunta al usuario si desea continuar analizando el entorno
        if continuar == "1":
            print("Continuando el análisis... \n") 

        elif continuar == "2":
            print("Deteniendo el análisis... \n")
            print("Hasta luego!\n")
            analizar = 0
        else:
            print("Opción no válida. Debe ingresar 1 o 2. \n")
            continuar = input("¿Deseas continuar analizando el entorno? (1 para continuar, 2 para detener): \n")
            if continuar == "1":
                print("Continuando el análisis... \n") 
            elif continuar == "2":
                print("Deteniendo el análisis... \n")
                print("Hasta luego!\n")
                analizar = 0

if mode == "1":
    print("Muy bien, te daré mi asistencia. \n")
    analizar(imagenes)
elif mode == "2":
    print("\nHasta luego! \n")
else:
    print("Opción no válida. Debe ingresar 1 o 2. \n")