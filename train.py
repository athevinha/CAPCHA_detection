import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
import glob
import string
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

folder = ['1', '2', '3', '4', '5', '6', '7',
          '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


def convertChar2Int(Y_TV):
    for i, Y in enumerate(Y_TV):
        if(Y == 'A'):
            Y = 10
        if(Y == 'B'):
            Y = 11
        if(Y == 'C'):
            Y = 12
        if(Y == 'D'):
            Y = 13
        if(Y == 'E'):
            Y = 14
        if(Y == 'F'):
            Y = 15
        Y_TV[i] = int(Y)
    return(Y_TV)


# =================GET DATA 1 -> 'F'==============================
Y_train = np.array([])
X_train = np.full((2912, 28, 28), 1)
print('Loading Data...')
for i in range(2912):
    Y_train = np.append(Y_train, '', axis=None)
print('Get Data...')
y = 0
for i in folder:
    for img in glob.glob("./DATA_TRAIN/" + i + '/*.png'):
        print('folder:', i, ' y ->', y)
        n = cv2.imread(img)
        n = cv2.cvtColor(n, cv2.COLOR_BGR2GRAY)
        n = cv2.resize(src=n, dsize=(28, 28))
        X_train[y] = n
        Y_train[y] = i
        y += 1
print('-----Get Data Successfully-----')
X_val, Y_val = X_train[2812:2912, :], Y_train[2812:2912]  # numpy
X_train, Y_train = X_train[:2812, :], Y_train[:2812]  # numpy
# =======================Shape data==========================

X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_val = X_val.reshape(X_val.shape[0], 28, 28, 1)
# =======================One hot=============================
Y_train = convertChar2Int(Y_train)
Y_val = convertChar2Int(Y_val)
Y_train = np_utils.to_categorical(Y_train, 16)
Y_val = np_utils.to_categorical(Y_val, 16)
print('Y train:', Y_train.shape)
print('X train:', X_train.shape)
print('Y val:', Y_val.shape)
print('X val:', X_val.shape)
# ?????nh ngh??a model
model = Sequential()

# Th??m Convolutional layer v???i 32 kernel, k??ch th?????c kernel 3*3
# d??ng h??m sigmoid l??m activation v?? ch??? r?? input_shape cho layer ?????u ti??n
model.add(Conv2D(32, (3, 3), activation='sigmoid', input_shape=(28, 28, 1)))

# Th??m Convolutional layer
model.add(Conv2D(32, (3, 3), activation='sigmoid'))

# Th??m Max pooling layer
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten layer chuy???n t??? tensor sang vector
model.add(Flatten())

# Th??m Fully Connected layer v???i 128 nodes v?? d??ng h??m sigmoid
model.add(Dense(128, activation='sigmoid'))

# Output layer v???i 10 node v?? d??ng softmax function ????? chuy???n sang x??c xu???t.
model.add(Dense(16, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
H = model.fit(X_train, Y_train, validation_data=(X_val, Y_val),
              batch_size=74, epochs=10, verbose=1)
# 8. V??? ????? th??? loss, accuracy c???a traning set v?? validation set

fig = plt.figure()
numOfEpoch = 10
print(H.history)
plt.plot(np.arange(0, numOfEpoch), H.history['loss'], label='training loss')
plt.plot(np.arange(0, numOfEpoch),
         H.history['val_loss'], label='validation loss')
plt.plot(np.arange(0, numOfEpoch), H.history['accuracy'], label='accuracy')
plt.plot(np.arange(0, numOfEpoch),
         H.history['val_accuracy'], label='validation accuracy')
plt.title('Accuracy and Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss|Accuracy')
plt.legend()
plt.show()
# model.save('model.ckpt')
