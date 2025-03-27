library(keras)
library(tensorflow)
library(ggplot2)
library(gridExtra)
library(png)

# Configuración inicial
dataset_path <- "C:/Users/aasal/OneDrive/Documentos/Curso Samsung/.venv/IA uni/Alfabeto/dateset400"
epochs <- as.integer(10)  # o simplemente 10L
batch_size <- as.integer(32)
target_size <- c(32, 32)  # Ajustar a vector numérico simple
classes <- c("A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y")

# 1. Preprocesamiento y aumento de datos
train_datagen <- image_data_generator(
  rescale = 1 / 255,  # Normalización de píxeles
  rotation_range = 20,  # Rotación aleatoria
  width_shift_range = 0.2,  # Desplazamiento horizontal aleatorio
  height_shift_range = 0.2,  # Desplazamiento vertical aleatorio
  horizontal_flip = TRUE,  # Volteo horizontal aleatorio
  validation_split = 0.2  # 20% de los datos para validación
)

# Generadores de datos
train_generator <- flow_images_from_directory(
  directory = dataset_path,
  generator = train_datagen,
  target_size = target_size,
  color_mode = "grayscale",
  batch_size = batch_size,
  class_mode = "categorical",
  classes = classes,
  subset = "training",
  seed = 123
)

validation_generator <- flow_images_from_directory(
  directory = dataset_path,
  generator = train_datagen,
  target_size = target_size,
  color_mode = "grayscale",
  batch_size = batch_size,
  class_mode = "categorical",
  classes = classes,
  subset = "validation",
  seed = 123
)

# 2. Construir el modelo
inputs <- layer_input(shape = c(32, 32, 1))  # Ajustar para incluir canal (grayscale)

outputs <- inputs %>%
  layer_conv_2d(filters = 32, kernel_size = c(3, 3), activation = "relu") %>%
  layer_max_pooling_2d(pool_size = c(2, 2)) %>%
  layer_conv_2d(filters = 64, kernel_size = c(3, 3), activation = "relu") %>%
  layer_max_pooling_2d(pool_size = c(2, 2)) %>%
  layer_conv_2d(filters = 128, kernel_size = c(3, 3), activation = "relu") %>%
  layer_max_pooling_2d(pool_size = c(2, 2)) %>%
  layer_flatten() %>%
  layer_dense(units = 128, activation = "relu") %>%
  layer_dense(units = length(classes), activation = "softmax")  # Ajustar salida para múltiples clases

model <- keras_model(inputs = inputs, outputs = outputs)

# 3. Compilar el modelo
model$compile(
  optimizer = optimizer_adam(),
  loss = "categorical_crossentropy",  # Cambiado a categorical_crossentropy
  metrics = list("accuracy")
)

# Resumen del modelo
summary(model)

# Callbacks
checkpoint_dir <- "C:/Users/aasal/OneDrive/Documentos/Curso Samsung/.venv/IA uni/Alfabeto/save"
if (!dir.exists(checkpoint_dir)) {
  dir.create(checkpoint_dir, recursive = TRUE)
}

checkpoint_callback <- callback_model_checkpoint(
  filepath = file.path(checkpoint_dir, "weights-{epoch:02d}-{val_accuracy:.2f}.h5"),  # Cambiado a .h5
  monitor = "val_accuracy",
  save_best_only = TRUE,
  mode = "max",
  verbose = 1
)

early_stop <- callback_early_stopping(
  monitor = "val_loss",
  patience = 5,
  restore_best_weights = TRUE
)

# 4. Entrenar el modelo
history <- model$fit(
  train_generator,
  epochs = epochs,  # Usar la variable definida
  validation_data = validation_generator,
  callbacks = list(checkpoint_callback, early_stop),
  verbose = 1
)

# 5. Evaluar el modelo
evaluation <- model$evaluate(validation_generator)
cat(sprintf("Pérdida en validación: %.4f\n", evaluation["loss"]))
cat(sprintf("Precisión en validación: %.4f\n", evaluation["accuracy"]))

# 6. Guardar el modelo
save_model_hdf5(model, "modelo_cajas.h5")
(str(generator_next(train_generator)))