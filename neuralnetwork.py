# -*- coding: utf-8 -*-
"""NeuralNetwork.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EBHwiwh3yXa4BLXWrmpjz1bcuPYtvn3I
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

# Loading the dataset
file_path = '/content/drive/MyDrive/BTP/train.csv'
data = pd.read_csv(file_path)

# Displaying the first few rows of the dataset
data.head()

"""tf-idf model"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import ast

# Converting the string representation of lists into actual lists.
data['ingredients'] = data['ingredients'].apply(ast.literal_eval)

data['ingredients_text'] = data['ingredients'].apply(lambda x: ' '.join(x))
data.head()

# Applying TF-IDF transformation
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(data['ingredients_text'])

# Encoding the labels (cuisines)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(data['cuisine'])

# Spliting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

cuisines = ['brazilian', 'british', 'cajun_creole', 'chinese', 'filipino', 'french', 'greek', 'indian', 'irish', 'italian', 'jamaican', 'japanese', 'korean', 'mexican', 'moroccan', 'russian', 'southern_us', 'spanish', 'thai', 'vietnamese']

import tensorflow

model = tensorflow.keras.models.Sequential([
    tensorflow.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tensorflow.keras.layers.Dropout(0.5),
    tensorflow.keras.layers.Dense(64, activation='relu'),
    tensorflow.keras.layers.Dropout(0.5),
    tensorflow.keras.layers.Dense(20, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

X_train_dense = X_train.toarray()
# y_train_dense = y_train.toarray()
X_test_dense = X_test.toarray()
# y_test_dense = y_test.toarray()

# Training the model using these sets
history = model.fit(X_train_dense, y_train, epochs=50, batch_size=128, validation_data=(X_test_dense, y_test))

import matplotlib.pyplot as plt

# This training is for all the cuisine identification

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

print(history.history['accuracy'])

import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()
file = r'/content/drive/MyDrive/BTP/train (1).json'
with open(file) as train_file:
    dict_train = json.load(train_file)

print(dict_train[0])

all_ing = []
total_ing = 0
x = 0
for i in dict_train:
  # if i["cuisine"] == 'mexican' or i["cuisine"] == 'italian':
    all_ing.extend(i["ingredients"])
    all_ing = list(set(all_ing))
    total_ing += len(i["ingredients"])
    x+=1

"""Changing one recipe to all cuisines"""

change_id = int(input())
test = dict_train[change_id]

test_dict = []
for i in range(len(test["ingredients"])):
  for j in all_ing:
    temp_ing = test["ingredients"].copy()
    if j not in temp_ing:
      temp_ing[i] = j
      test_dict.append(temp_ing)

print(test_dict[change_id])
print(len(test_dict))

new_lis = []
for i in test_dict:
  temp = ""
  for j in i:
    temp += j
    temp += " "
  new_lis.append(temp)
print(new_lis[change_id])

print(len(new_lis))

X_temp = tfidf.fit_transform(new_lis)
X_temp1 = X_temp.toarray()
final_res = model.predict(X_temp1)

print(final_res.shape)

fin = -1
all_cuisine = []
for j in range(20):
  for i in range(len(final_res)):
    m = max(final_res[i])
    if list(final_res[i]).index(m) == j and m>final_res[fin][j]:
      fin = i
  all_cuisine.append(final_res[fin])


print(len(all_cuisine))
for i in range(len(all_cuisine)):
  print("{} : {}".format(cuisines[i], all_cuisine[i][i]))

# The printed numbers mean the maximum amount of similarity we could achieve by transforming the original recipe from the source cuisine to the
# transformed recipe which belongs to the target cuisine.

"""word2vec model"""

from gensim.models import Word2Vec

# Flattening the list of ingredients
all_ingredients = [ingredient for ingredients_list in data['ingredients'] for ingredient in ingredients_list]
print(len(all_ingredients))
# Training the Word2Vec model
model = Word2Vec([all_ingredients], vector_size=10, window=3, min_count=1, workers=4)

# Vectorizing the ingredients per recipe
# We'll average the vectors of the ingredients for each recipe
def vectorize_ingredients(ingredients_list):
    vector = sum([model.wv[ingredient] for ingredient in ingredients_list if ingredient in model.wv]) / len(ingredients_list)
    return vector

data['ingredients_vector'] = data['ingredients'].apply(vectorize_ingredients)


data.head()

print(data['ingredients'][0])
print(data['ingredients_vector'][0])

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

# Converting the vectors to a numpy array
vectors = np.array(data['ingredients_vector'].tolist())

# Label Encoding
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(data['cuisine'])

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size=0.2, random_state=42)

# Checking the shape of the training and testing data
X_train.shape, X_test.shape, y_train.shape, y_test.shape

import tensorflow as tf
import keras


# model1 = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(512, activation='relu', input_shape=(100,), kernel_regularizer=tf.keras.regularizers.l2(0.001)),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.BatchNormalization(),
#     tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.BatchNormalization(),
#     tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.BatchNormalization(),
#     tf.keras.layers.Dense(20, activation='softmax')
# ])


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(20, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

history = model.fit(X_train, y_train, epochs=50, batch_size=128, validation_data=(X_test, y_test), callbacks=[early_stopping])

model.summary()

from sklearn.metrics import f1_score
import numpy as np

yhat_test = model.predict(X_test_dense)

yhat_test_pred = np.argmax(yhat_test, axis=1)

print(f1_score(y_test, yhat_test_pred, average=None))
print(f1_score(y_test, yhat_test_pred, average='weighted'))

from keras.utils.vis_utils import plot_model
plot_model(model, show_shapes=True, show_layer_names=True)

!pip3 install ann_visualizer

!pip install graphviz

!pip install keras

from ann_visualizer.visualize import ann_viz;

ann_viz(model, title="My first neural network")
