import orionconnection
import rollingwindow
from keras.models import model_from_json
from keras.layers import Flatten, LSTM, Dense, Activation
from keras.layers.convolutional import MaxPooling1D, Conv1D
from keras.models import Sequential
from numpy import array

def getModelCNNWindow3(sequence, window_size=3, n_features=1,epochs=100):
    model = Sequential()
    model.add(Conv1D(filters=24, kernel_size=2, activation='relu', input_shape=(window_size, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    X, y = rollingwindow.split_sequence(sequence, window_size)
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    
    model.fit(X, y, epochs=epochs)

    return model


def getModelCNNWindow24(sequence, window_size=int(24), activation='relu', n_features=1, epochs=100 ):
    
    kernel_size = [2,2]
    filters = [6,6]
    pool_size = [2,2]
    
    model = Sequential()
    model.add(Conv1D(filters=filters[0],
                     kernel_size=kernel_size[0],
                     activation='relu',
                     input_shape=(window_size, n_features)))
    model.add(MaxPooling1D(pool_size=pool_size[0]))
    model.add(Activation('relu'))
    model.add(Conv1D(filters=filters[1],
                     kernel_size=kernel_size[1],
                     activation='relu',
                     input_shape=(window_size, n_features)))
    model.add(MaxPooling1D(pool_size=pool_size[1]))
    model.add(Activation('relu'))

    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
   
    model.compile(optimizer='adam', loss='mse')
    X, y = rollingwindow.split_sequence(sequence, window_size)
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    
    model.fit(X, y, epochs=epochs)
    
    return model

def getModelCNNLSTM(sequence, window_size=3, n_features=1, epochs=30):
    model = Sequential()
    model.add(Conv1D(filters=24, kernel_size=2, activation='relu', input_shape=(window_size, n_features)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(LSTM(units=10,activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer='glorot_uniform'))
    
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    X, y = rollingwindow.split_sequence(sequence, window_size)
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    
    model.fit(X, y, epochs=epochs)

    return model

def getModelLSTM(sequence, window_size=3, n_features=1, epochs=30):
    model = Sequential()
    model.add(LSTM(units=10,activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer='glorot_uniform'))
    
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    X, y = rollingwindow.split_sequence(sequence, window_size)
    X = X.reshape((X.shape[0], X.shape[1], n_features))
    
    model.fit(X, y, epochs=epochs)

    return model


def predict_next(model, window, window_size):
    window = array(window)
    window = window.reshape(1, window_size, 1)
    return model.predict(window)


def saveModel(model, filename, weights_name):
    model_json = model.to_json()
    with open(filename, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(weights_name)

def getModel(filename, weights_name):
    json_file = open(filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(weights_name)
    loaded_model.compile(optimizer='adam', loss='mse')
    return loaded_model