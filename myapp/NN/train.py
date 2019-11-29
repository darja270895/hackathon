import pyexcel as pe
import numpy
from sklearn.preprocessing import LabelBinarizer
from keras.models import Sequential
from keras.layers import Dense



dataset = pe.get_array(file_name = 'dataset.xls')

new_list = []
for i in dataset:
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


y_arr = numpy.asarray(dataset)
y = y_arr[:, 11]
encoder = LabelBinarizer()
y_categorial = encoder.fit_transform(y)


model = Sequential()
model.add(Dense(11, input_shape=(11, ), activation='relu'))
model.add(Dense(6, activation='relu'))
model.add(Dense(7, activation='relu'))
model.add(Dense(14, activation='relu'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(xarr, y_categorial, epochs=150, batch_size=10)


_, accuracy = model.evaluate(xarr, y_categorial)
print('Accuracy: %.2f' % (accuracy*100))


model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
