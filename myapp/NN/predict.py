from keras.models import model_from_json
import pyexcel as pe
import numpy
from sklearn.preprocessing import LabelBinarizer


class Predict():
    def __init__(self, dataset=pe.get_array(file_name='dataset.xls')):

        self.excel_dataset = pe.get_array(file_name='dataset.xls')
        self.dataset = dataset
        self.classes = []

    def predict_data(self):

        new_list = []
        for i in self.dataset:
            temp = []
            for j in i:
                byt = j.encode('utf-8')
                to_int = int.from_bytes(byt, "big")
                to_float = float.fromhex(hex(to_int))
                temp.append(to_float)
            new_list.append(temp)

        arr = numpy.asarray(new_list)

        x = arr[:, 0:11]
        xarr = x - x.mean()
        xarr = xarr / xarr.max()

        y_arr = numpy.asarray(self.excel_dataset)
        y = y_arr[:, 11]
        encoder = LabelBinarizer()
        y_categorial = encoder.fit_transform(y)

        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()

        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights("model.h5")

        loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

        # score = loaded_model.evaluate(xarr, y_categorial, verbose=0)
        # print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))

        predictions = loaded_model.predict(xarr)
        predictions_class = loaded_model.predict_classes(xarr)

        self.classes = encoder.classes_

        # print(self.classes)
        # print(' {} => class - {} name {} (expected {})'.format(predictions, predictions_class, encoder.classes_[predictions_class], y_categorial))
        # print("Prediction: {}".format(encoder.classes_[predictions_class][0]))

        return encoder.classes_[predictions_class][0]

        # for i in range(5):
        #     print(' {} => class - {} name {} (expected {})'.format(predictions[i], predictions_class[i], encoder.classes_[predictions_class[i]],  y_categorial[i]))


p = Predict([['нейтральные комфортные дни', 'не уверен, удивите меня', 'парой', 'всего понемногу',
              'необычные местные блюда', 'не имеет значения', 'командные, игровые', 'места с историей',
              'отдых от работы и людей', 'две недели', 'в туристической части города']])

a = p.predict_data()
print(a)
