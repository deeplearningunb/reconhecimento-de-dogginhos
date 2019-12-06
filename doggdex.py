#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 09:53:12 2019
@author: cfnunes
"""

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras import backend as K
import numpy as np
import pickle
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
 # Convolutional Neural Network

# Part 1 - Building the CNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# load the labels of train set (generated by "get_features.py")
Y_train = np.load('train_labels.npy')

# load the bottleneck features (generated by "get_features.py")
X_train = np.load('bottleneck_features_train.npy')
X_test = np.load('bottleneck_features_test.npy')

# Initialising the CNN
classifier = Sequential()

classifier.add(Flatten(input_shape = X_train.shape[1:]))
classifier.add(Dropout(0.5))
classifier.add(Dense(units = 32, activation = 'relu'))
classifier.add(Dropout(0.5))
classifier.add(Dense(units = 14, activation = 'softmax'))
classifier.summary()

classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Part 2 - Fitting the CNN to the images

# train_datagen = ImageDataGenerator(rescale = 1./255,
#                                 shear_range = 0.2,
#                                 zoom_range = 0.2,
#                                 horizontal_flip = True)
#
# test_datagen = ImageDataGenerator(rescale = 1./255)
#
# training_set = train_datagen.flow_from_directory('./dataset/training_dataset/train/',
#                                                 target_size = (64, 64),
#                                                 batch_size = 512,
#                                                 class_mode = 'categorical')
#
# test_set = test_datagen.flow_from_directory('./dataset/test_dataset/test/',
#                                             target_size = (64, 64),
#                                             batch_size = 512,
#                                             class_mode = 'categorical')

# classifier.fit_generator(training_set,
#                         steps_per_epoch = 150,
#                         epochs = 200,
#                         validation_data = test_set,
#                         validation_steps = 200
#                         )

test_image = image.load_img('test/test/test_image.png', target_size=(299, 299))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)


#classifier.fit_generator(
#    X_train,
#    steps_per_epoch = 100,
#    validation_data = Y_train,
#    epochs=10,
#    validation_steps = 20
#)

classifier.fit(X_train, Y_train, validation_split=0.1, epochs=50, batch_size=512, verbose=1)

# ========= SAVE MODEL ===============
filename = 'training_oil_savemodel.sav'
file = open(filename, 'wb')
pickle.dump(classifier, file)

file.close()

#=================== PREDICTION =================

#train_datagen = ImageDataGenerator(rescale = 1./255,
#                                         shear_range = 0.2,
#                                         zoom_range = 0.2,
#                                         horizontal_flip = True)
#
#test_datagen = ImageDataGenerator(rescale = 1./255)
#
#training_set = train_datagen.flow_from_directory('./dataset/training_dataset/train/',
#                                                 target_size = (64, 64),
#                                                 batch_size = 128,
#                                                 class_mode = 'categorical')
#
#test_set = test_datagen.flow_from_directory('./test/',
#                                             target_size = (64, 64),
#                                             batch_size = 128,
#                                             class_mode = 'categorical')

#file = open(filename, 'rb')
#loaded_model = pickle.load(file)
loaded_model = classifier
#loss, metric = loaded_model.evaluate_generator(generator=test_set, steps=80)
#print("Acurácia:" + str(metric))
test_image = np.vstack([test_image])

model = InceptionResNetV2(include_top=False, weights='imagenet')

result = loaded_model.predict(X_test)
result = result[0]
#classes = training_set.class_indices
#print(X_train.__dict__)
print(result)
print('*'*100)

greater = -1
value = -1
i = 0

for res in result:
    if greater < res:
        greater = res
        value = i
    i += 1

print(greater)
print(value)


counter = 0
for item in classes.keys():
    classes[item] = result[counter]
    counter += 1

results = [classes[item] for item in classes.keys()]

greater = [
    'init',
    -1
]

for breeddog in training_set.class_indices.keys():
    if training_set.class_indices[breeddog] > greater[1]:
        greater[0] = breeddog
        greater[1] = training_set.class_indices[breeddog]

print(greater)
print(training_set.class_indices)
