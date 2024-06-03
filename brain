from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam

class Brain:
    def __init__(self, iS=(15, 15, 4), lr=0.0005):  # Updated input shape
        self.learningRate = lr
        self.iS = iS
        self.numOutputs = 4
        self.model = Sequential()

        # Adding layers to the model
        self.model.add(Conv2D(4, (3, 3), activation='relu', input_shape=self.iS))
        self.model.add(MaxPooling2D((2, 2)))
        self.model.add(Conv2D(4, (2, 2), activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(units=4, activation='relu'))
        self.model.add(Dense(units=self.numOutputs))
        self.model.compile(loss="mean_squared_error", optimizer=Adam(learning_rate=self.learningRate))

    def load_model(self, file_path):
        self.model = load_model(file_path)
        return self.model
