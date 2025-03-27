# Nombre del Programa: Sistema experto traductor para sordos                      #
# Autor: Guillermo Cardenas, Juan Suarez  .                                       #
# Versión: 5.4.6.B                                                                #
# Descripción: Sistema donde se corre el modelo de red convolucional              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
from mss import mss

# Cargar el modelo entrenado
model = tf.keras.models.load_model("Modelo_lenguje_senas_5.keras")

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Etiquetas de las clases (excluyendo J y Z)
class_labels = "ABCDEFGHIKLMNOPQRSTUVWXY"

# Función para preprocesar la imagen
def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    image = cv2.resize(image, (28, 28))  # Redimensionar a 28x28
    image = image / 255.0  # Normalizar
    image = image.reshape(1, 28, 28, 1)  # Reformar para el modelo
    return image

# Función para predecir la clase de la imagen
def predict_image(image):
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction)
    return predicted_class, confidence

# Configurar la captura de pantalla con mss
with mss() as sct:
    # Definir el área de captura (600x600 píxeles centrados)
    screen_width = sct.monitors[1]["width"]
    screen_height = sct.monitors[1]["height"]
    monitor = {
        "top": (screen_height - 600) // 2,  # Centrar verticalmente
        "left": (screen_width - 600) // 2,   # Centrar horizontalmente
        "width": 600,
        "height": 600
    }

    print("Captura de pantalla activada. Presiona 'q' para salir.")

    while True:
        # Capturar el recuadro de la pantalla
        screenshot = np.array(sct.grab(monitor))

        # Convertir la imagen a RGB (MediaPipe requiere imágenes en RGB)
        rgb_frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)

        # Procesar el frame con MediaPipe Hands
        results = hands.process(rgb_frame)

        # Si se detecta una mano, dibujar un recuadro azul alrededor de ella
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Obtener las coordenadas de los landmarks de la mano
                h, w, _ = screenshot.shape
                x_min, y_min, x_max, y_max = w, h, 0, 0
                for landmark in hand_landmarks.landmark:
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    if x < x_min:
                        x_min = x
                    if x > x_max:
                        x_max = x
                    if y < y_min:
                        y_min = y
                    if y > y_max:
                        y_max = y

                # Dibujar un recuadro azul alrededor de la mano
                cv2.rectangle(screenshot, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

                # Recortar la región de la mano
                hand_region = screenshot[y_min:y_max, x_min:x_max]

                # Si la región de la mano es válida, preprocesarla y predecir
                if hand_region.size != 0:
                    processed_image = preprocess_image(hand_region)
                    predicted_class, confidence = predict_image(processed_image)

                    # Verificar que predicted_class esté dentro del rango válido
                    if 0 <= predicted_class < len(class_labels):
                        label = f"Prediccion: {class_labels[predicted_class]} (Confianza: {confidence:.2f})"
                    else:
                        label = "Prediccion: Desconocido"

                    # Mostrar la predicción en el frame
                    cv2.putText(screenshot, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Mostrar el frame en una ventana
        cv2.imshow('Captura de Pantalla - Detección de Manos', screenshot)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()