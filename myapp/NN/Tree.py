from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
import graphviz
import pyexcel as pe
import os
from sklearn.preprocessing import LabelBinarizer
from collections import Counter
import numpy

# iris_data = load_iris()
# print(type(iris_data))



def path():
    path = os.path.abspath(__file__)
    test_dataset = path.replace('train.py', 'test_dataset.xls')
    dataset = path.replace('train.py', 'dataset.xls')
    model = path.replace('train.py', 'model.h5')
    j_models = path.replace('train.py', 'model.json')
    return test_dataset, dataset, model, j_models

class Train:
    def __init__(self, dataset=pe.get_array(file_name=path()[1])):
        self.dataset = dataset
        self.x = []
        self.y_categorical = []
        self.numb_arr = []
        self.set_list = []

    def set_x(self):

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
        print(new_arr)

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

        for i in range(length):  # col
            temp_list = []
            for j in range(len(self.dataset)):  # rows
                for counter in range(len(self.set_list[i])):
                    if new_arr[i][j] == self.set_list[i][counter]:
                        temp_list.append(counter)
                    else:
                        ...

            self.numb_arr.append(temp_list)

        # set_x
        x = numpy.asarray(self.numb_arr)
        x = x[0:11]
        self.x = numpy.reshape(x, (x.shape[1], x.shape[0]))

    def set_y(self):

        y_arr = numpy.asarray(self.dataset)
        y = y_arr[:, 11]
        encoder = LabelBinarizer()
        self.y_categorial = encoder.fit_transform(y)

    # def train(self):
    #
    #     self.model.add(Dense(11, input_shape=(11,), activation='relu'))
    #     self.model.add(Dense(1000, activation='relu'))
    #     self.model.add(Dropout(0.5))
    #     self.model.add(Dense(500, activation='relu'))
    #     self.model.add(Dropout(0.5))
    #     self.model.add(Dense(self.y_categorial.shape[1], activation='softmax'))
    #
    #     # boosting
    #
    #     # fscore   yandex catboost - for categorial data
    #
    #     self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', ])
    #     self.model.fit(self.x, self.y_categorial, epochs=500, batch_size=16)
    #     _, accuracy = self.model.evaluate(self.x, self.y_categorial)
    #     print('Accuracy: %.2f' % (accuracy * 100))
    #


if __name__ == ('__main__'):
    t = Train()
    t.set_x()
    t.set_y()
    # t.train()



#
# tree = DecisionTreeClassifier()
#
# # tree = tree.fit(iris_data.data, iris_data.target)
# print("Accurancy: {}".format(tree.score(iris_data.data, iris_data.target)))


# dot_data = tree.export_graphviz(classification_tree, out_file=None,
#                      feature_names=iris_data.feature_names,
#                      class_names=iris_data.target_names,
#                      filled=True, rounded=True,
#                      special_characters=True)
# graph = graphviz.Source(dot_data)
# graph.render("iris")