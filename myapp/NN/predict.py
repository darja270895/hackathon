from keras.models import model_from_json
import pyexcel as pe
import numpy
from sklearn.preprocessing import LabelBinarizer
# from collections import Counter
# import keras.losses as losses
from train import Train


class Predict():
    def __init__(self, dataset=pe.get_array(file_name='test_dataset.xls')):
        self.excel_dataset = pe.get_array(file_name='dataset.xls')
        self.dataset = dataset
        self.classes = []
        self.set_list = []
        self.numb_arr = []
        self.x = []

    def predict_data(self):

        print(self.dataset)
        t = Train()
        t.set_x()
        self.set_list = t.set_list
        numb_arr = []
        length = len(self.dataset[0])
        # print(len(self.dataset))
        # print(length)

        arr = numpy.asarray(self.dataset)
        length = len(arr[0])
        new_arr = []
        # swapp arr
        for column in range(length):
            temp_arr = []
            for row in range(len(arr)):
                temp_arr.append(self.dataset[row][column])
            new_arr.append(temp_arr)

        new_arr = numpy.asarray(new_arr)
        # print(new_arr)

        for i in range(length):  # col - 11
            temp_list = []
            for j in range(len(self.dataset)):  # rows - 1
                for counter in range(len(self.set_list[i])): # - 12 5
                    if new_arr[i][j] == self.set_list[i][counter]:
                        temp_list.append(counter)
                    else:
                        ...

            self.numb_arr.append(temp_list)

        self.x = numpy.asarray(self.numb_arr)
        self.x = numpy.reshape(self.x, (self.x.shape[1], self.x.shape[0]))


        encoder = LabelBinarizer()

        y_arr = numpy.asarray(self.excel_dataset)
        y = y_arr[:, 11]

        encoder.fit_transform(y)
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("model.h5")
        loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # predictions = loaded_model.predict(self.x)
        predictions_class = loaded_model.predict_classes(self.x)
        self.classes = encoder.classes_

        # print(self.classes)
        # print(' {} => class - {} name {} (expected {})'.format(predictions, predictions_class, encoder.classes_[predictions_class], y_categorial))
        # print("Prediction: {}".format(encoder.classes_[predictions_class][0]))

        # for i in range(5):
        #     print(' {} => class - {} name {} (expected {})'.format(predictions[i], predictions_class[i], encoder.classes_[predictions_class[i]],  y_categorial[i]))


        return encoder.classes_[predictions_class][0]


p0 = Predict([['нейтральные комфортные дни', 'не уверен, удивите меня', 'парой', 'всего понемногу',
              'необычные местные блюда', 'не имеет значения', 'командные, игровые', 'места с историей',
              'отдых от работы и людей', 'две недели', 'в туристической части города']])
a0 = p0.predict_data()
print(a0)



# p = Predict([['настоящая зима и много снега', 'ленивый', 'парой', 'спорт', 'необычные местные блюда',
#               'несколько ( до 6) часов', 'командные, игровые', 'причудливые и максимально необычные', 'отдых от работы и людей', 'на неделю',
#               'нет предпочтений']])
# a = p.predict_data()
# print(a)
#

p1 = Predict([['нейтральные комфортные дни', 'не уверен, удивите меня', 'парой', 'всего понемногу',
               'необычные местные блюда', 'не имеет значения', 'командные, игровые', 'места с историей',
               'отдых от работы и людей', 'на уикэнд', 'в туристической части города']])
a1 = p1.predict_data()
print(a1)

