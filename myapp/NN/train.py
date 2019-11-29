import pyexcel as pe
import numpy
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from keras.models import Sequential
from keras.layers import Dense



dataset = pe.get_array(file_name='test_dataset.xls')




new_list = []
for i in dataset:
    temp = []
    for j in i:
        byt = j.encode('utf-8')
        to_int = int.from_bytes(byt, "big")
        to_float = float.fromhex(hex(to_int))
        temp.append(to_float)
    new_list.append(temp)

# xx = numpy.array(new_list, dtype=numpy.float64)[:, 0:11]
#
# sc = StandardScaler()
# XN = sc.fit_transform(xx)
# print(XN)
# print("______________")

arr = numpy.asarray(new_list)
x = arr[:, 0:11]


maxim_list = []
for k in new_list:
   maxim_list.append(max(k))

maxim_value = max(maxim_list)

x_new = []
for iter_list in x:
    mean = iter_list.mean()
    for iter in iter_list:
        print((iter - mean) / maxim_value)



xarr = x - x.mean()
xarr = xarr / maxim_value

print("___________")
print(xarr)

y_arr = numpy.asarray(dataset)
y = y_arr[:, 11]
encoder = LabelBinarizer()
y_categorial = encoder.fit_transform(y)


# model = Sequential()
# model.add(Dense(11, input_shape=(11, ), activation='relu'))
# model.add(Dense(50, activation='relu'))
# model.add(Dense(3, activation='relu'))
#
# model.compile(loss='mse', optimizer='adam', metrics=['accuracy', 'mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error'])
# model.fit(xarr, y_categorial, epochs=300, batch_size=50)
#
#
# _, accuracy = model.evaluate(xarr, y_categorial)
# print('Accuracy: %.2f' % (accuracy*100))
#
#
# model_json = model.to_json()
# with open("model.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# model.save_weights("model.h5")
# print("Saved model to disk")
