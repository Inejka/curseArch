import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import keras
from keras_visualizer import visualizer
from tensorflow.keras.utils import plot_model


class model:
    def __init__(self, voc_size, epoch, first_optimizer="rmsprop", second_optimizer="adam", local=False):
        self.voc_size = voc_size
        self.epoch = epoch
        self.model_time = Sequential()
        self.model_time.add(Dense(max(voc_size / 2, 8), input_dim=voc_size, activation='relu'))
        if not local:
            self.model_time.add(Dense(max(voc_size / 4, 6), activation='sigmoid'))
            self.model_time.add(Dense(max(voc_size / 8, 4), activation='relu'))
            self.model_time.add(Dense(max(voc_size / 16, 2), activation='sigmoid'))
        self.model_time.add(Dense(1, activation='linear'))
        self.model_time.compile(loss='mean_squared_error', optimizer=first_optimizer, metrics=['mean_squared_error'], )
        self.model_class = Sequential()
        self.model_class.add(Dense(max(voc_size, 1), input_dim=voc_size, activation='sigmoid'))
        self.model_class.add(Dense(max(voc_size / 16, 1), activation='sigmoid'))
        self.model_class.add(Dense(1, activation='sigmoid'))
        self.model_class.compile(loss='binary_crossentropy', optimizer=second_optimizer, metrics=['accuracy'])

    def fit(self, X, Y):
        time_X = []
        time_Y = []
        for i, j in zip(X, Y):
            if j > 0:
                time_X.append(i)
                time_Y.append(j)
        time_X = np.array(time_X).astype('float32')
        time_Y = np.array(time_Y).astype('float32')
        class_X = np.array(X).astype('float32')
        class_Y = np.array(Y).astype('float32')
        class_Y = np.where(class_Y > 0, 1, 0)
        self.model_time.fit(time_X, time_Y, epochs=self.epoch, verbose=2)
        self.model_class.fit(class_X, class_Y, epochs=self.epoch // 15, verbose=2)

    def predict(self, X):
        X = np.array(X).astype('float32')
        temp = self.model_class.predict(X)
        temp = np.array(temp).astype('float32')
        for i in range(len(temp)):
            if temp[i] > 0.5:
                temp[i] = self.model_time.predict(np.array([X[i], ]))
            else:
                temp[i] = -1000
        return temp

    def save(self, path):
        self.model_time.save(path + "_time.net")
        self.model_class.save(path + "_class.net")

    def load(self, path):
        self.model_time = keras.models.load_model(path + "_time.net")
        self.model_class = keras.models.load_model(path + "_class.net")

    def get_null_vector(self):
        return self.model_time.predict(np.array([np.zeros(self.voc_size), ]))