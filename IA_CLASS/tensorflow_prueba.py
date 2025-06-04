import pandas as pd #use pandas to from excel file
import tensorflow as tf #use tensorflow
import numpy as np

# Loading data from excel file
def load_data(filename):
    df = pd.read_excel(filename)
    return df

# Preprocessing the data
def preprocess_data(df):
    # Convert country names to numerical labels
    country_names = df['Country'].tolist()
    # validate if the column 'Number' is in the dataframe
    if 'Number' in df.columns:
        country_numbers = df['Number'].astype(int).tolist() # Convert the 'Number' column to a list
    else:
        raise KeyError("The 'Number' column is missing from the DataFrame")
    
    return country_names, country_numbers #return the country names and country numbers

# Building the model of the neural network
def build_model(input_dim):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(1,)),
        tf.keras.layers.Dense(64, activation='relu'), # use relu as activation function with 64 neurons
        tf.keras.layers.Dense(32, activation='relu'), # second layer with 32 neurons
        tf.keras.layers.Dense(1, activation='linear') # output layer with 1 neuron
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error') # compile the model with adam optimizer and mean squared error loss function
    return model

def main():
    filename = 'countries_data.xlsx'
    df = load_data(filename)
    country_names, country_numbers = preprocess_data(df)
    
    # Convert country numbers to a numpy array
    X = tf.constant(country_numbers, dtype=tf.float32) # Convert the country numbers to a tensor
    y = tf.constant(country_numbers, dtype=tf.float32) # Convert the country numbers to a tensor
    
    model = build_model(input_dim=1)
    
    # Train the model
    model.fit(X, y, epochs=10, batch_size=1)
    
    # Perform a search
    search_number = 100  # Ejemplo de numero de busqueda
    prediction = model.predict(np.array([[search_number]]))  # Array 2D: [[100]]
    print(f"Predicción para {search_number}: {prediction[0][0]}")

if __name__ == '__main__':
    main()