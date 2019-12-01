import pyexcel as pe
import numpy
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.preprocessing.text import one_hot, text_to_word_sequence
from collections import Counter

class Train:
    def __init__(self, dataset = pe.get_array(file_name='dataset.xls')):
        self.dataset = dataset
        self.model = Sequential()
        self.x = []
        self.y_categorical = []
        self.numb_arr = []
        self.set_list = []

    def set_x(self):

        arr = numpy.asarray(self.dataset)
        length = len(arr[0])
        new_arr = []
        #swapp arr
        for column in range(length):
            temp_arr = []
            for row in range(len(arr)):
                temp_arr.append(self.dataset[row][column])
            new_arr.append(temp_arr)

        new_arr = numpy.asarray(new_arr)


        unique_list = []

        for counter in range(len(new_arr)):
            unique_list.append(len(Counter(new_arr[counter]).keys()))


        self.set_list = []  # list of indexes: unique values
        for elem in new_arr:
            data_list = [key for key in Counter(elem)]
            temp_dict = {i: data_list[i] for i in range(0, len(data_list))}
            self.set_list.append(temp_dict)

        # print(self.set_list)

        self.numb_arr = []

        for i in range(length): #col
            temp_list = []
            for j in range(len(self.dataset)): #rows
                for counter in range(len(self.set_list[i])):
                    if new_arr[i][j] == self.set_list[i][counter]:
                        temp_list.append(counter)
                    else:
                        ...

            self.numb_arr.append(temp_list)

        #set_x
        x = numpy.asarray(self.numb_arr)
        x = x[0:11]
        self.x = numpy.reshape(x, (x.shape[1], x.shape[0]))


    def set_y(self):

        y_arr = numpy.asarray(self.dataset)
        y = y_arr[:, 11]
        encoder = LabelBinarizer()
        self.y_categorial = encoder.fit_transform(y)

    def train(self):

        self.model.add(Dense(11, input_shape=(11, ), activation='relu'))
        self.model.add(Dense(200, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.y_categorial.shape[1], activation='softmax'))


        #fscore   yandex catboost - for categorial data

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', ])
        self.model.fit(self.x, self.y_categorial, epochs=500, batch_size=16)
        _, accuracy = self.model.evaluate(self.x, self.y_categorial)
        print('Accuracy: %.2f' % (accuracy*100))



    def serialize_model(self):
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        self.model.save_weights("model.h5")
        print("Saved model to disk")


if __name__ == ('__main__'):
    t = Train()
    t.set_x()
    t.set_y()
    t.train()
    t.serialize_model()