# Nombre del Programa: Sistema de entrenamiento de modelo de la red               #
# Autor: Guillermo Cardenas, Juan Suarez.                                         #
# Versión: 2                                                                      #
# Descripción: Sistema que entrena el modelo de red convolucional                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Importar las bibliotecas necesarias
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Cargar el dataset desde archivos CSV
train_df = pd.read_csv('Datos_csv\sign_mnist_train.csv')  # Cargar datos de entrenamiento
test_df = pd.read_csv('Datos_csv\sign_mnist_test.csv')    # Cargar datos de prueba

# Función para preprocesar los datos
def preprocess_data(df):
    # Extraer las etiquetas (labels) de la columna 'label'
    labels = df['label'].values
    # Extraer las imágenes (todas las columnas excepto 'label') y convertirlas a un array de numpy
    images = df.drop(columns=['label']).values
    # Reformar las imágenes a un formato de (28, 28, 1) para que sean compatibles con una CNN
    images = images.reshape(-1, 28, 28, 1)
    # Normalizar los valores de píxeles al rango [0, 1]
    images = images / 255.0
    return images, labels

# Preprocesar los datos de entrenamiento y prueba
X_train, y_train = preprocess_data(train_df)  # Preprocesar datos de entrenamiento
X_test, y_test = preprocess_data(test_df)     # Preprocesar datos de prueba

# Convertir las etiquetas a one-hot encoding
num_classes = 25  # Número de clases (24 letras del lenguaje de señas, excluyendo J y Z)
y_train = to_categorical(y_train, num_classes)  # Convertir etiquetas de entrenamiento
y_test = to_categorical(y_test, num_classes)    # Convertir etiquetas de prueba

# Definir el modelo de red neuronal convolucional (CNN)
model = models.Sequential([
    # Primera capa convolucional con 32 filtros de 3x3 y función de activación ReLU
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    # Capa de MaxPooling para reducir la dimensionalidad
    layers.MaxPooling2D((2, 2)),
    # Segunda capa convolucional con 64 filtros de 3x3 y función de activación ReLU
    layers.Conv2D(64, (3, 3), activation='relu'),
    # Otra capa de MaxPooling
    layers.MaxPooling2D((2, 2)),
    # Tercera capa convolucional con 128 filtros de 3x3 y función de activación ReLU
    layers.Conv2D(128, (3, 3), activation='relu'),
    # Última capa de MaxPooling
    layers.MaxPooling2D((2, 2)),
    # Capa de Dropout para evitar el sobreajuste (desactiva el 50% de las neuronas aleatoriamente)
    tf.keras.layers.Dropout(0.5),
    # Aplanar la salida para conectarla a una capa densa
    layers.Flatten(),
    # Capa densa (fully connected) con 128 neuronas y función de activación ReLU
    layers.Dense(128, activation='relu'),
    # Capa de salida con 'num_classes' neuronas (una por cada clase) y activación softmax
    layers.Dense(num_classes, activation='softmax')  # 24 clases (A-Y, excluyendo J y Z)
])

# Compilar el modelo
model.compile(optimizer='adam',               # Usar el optimizador Adam
              loss='categorical_crossentropy',  # Función de pérdida para clasificación multiclase
              metrics=['accuracy'])           # Métrica a monitorear: precisión

# Entrenar el modelo
history = model.fit(X_train, y_train,         # Datos de entrenamiento
                    epochs=10,                # Número de épocas
                    batch_size=32,            # Tamaño del lote
                    validation_data=(X_test, y_test))  # Datos de validación

# Evaluar el modelo en el conjunto de prueba
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print(f'\nPrecisión en el conjunto de prueba: {test_acc:.4f}')  # Mostrar la precisión en prueba

# Guardar el modelo entrenado en un archivo
model.save('Modelo_lenguje_senas_5.keras')  # Guardar el modelo en formato .keras