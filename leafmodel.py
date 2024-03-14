# -*- coding: utf-8 -*-
"""LeafModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1evmivAw1rwLB6B3bIBTy9ASbKnOhXKCb

# **Model**
"""

from keras.applications.vgg19 import VGG19
vgg_conv = VGG19(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

from keras.preprocessing.image import ImageDataGenerator

for layer in vgg_conv.layers[:-2]:
    layer.trainable = False

for layer in vgg_conv.layers:
    print(layer, layer.trainable)

from keras import models
from keras import layers
from tensorflow.keras import optimizers

model = models.Sequential()

model.add(vgg_conv)

model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(13, activation='softmax'))

model.summary()

train_dir =  '/content/drive/MyDrive/Leaf/Test'
validation_dir = '/content/drive/MyDrive/Leaf/Valid'

import numpy as np
from random import shuffle

from google.colab import drive
drive.mount('/content/drive')

from google.colab import drive
drive.mount('/content/drive')

train_datagen = ImageDataGenerator(rescale=1./255)

validation_datagen = ImageDataGenerator(rescale=1./255)

train_batchsize = 50
val_batchsize = 50

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=train_batchsize,
        class_mode='categorical')

validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(224, 224),
        batch_size=val_batchsize,
        class_mode='categorical',
        shuffle=True)

print(train_generator.class_indices)

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])


#try on different epoch, batch size, and the optimizer. Just to make the report clear
# present the loss and accuracy using line graph. On different set up.
# give me access on the file of the dataset.




history = model.fit_generator(
      train_generator,
      steps_per_epoch=train_generator.samples/train_generator.batch_size ,
      epochs=50,
      validation_data=validation_generator,
      validation_steps=validation_generator.samples/validation_generator.batch_size,
      verbose=1)

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

model.save('/content/drive/MyDrive/Leaf/leafvgg19.h5')

"""# **Prediction**"""

import numpy as np
import keras
import cv2
import matplotlib.pyplot as plt

# pip install termcolor

from termcolor import colored

from keras.models import load_model

model = load_model('/content/drive/MyDrive/Leaf/leafvgg19.h5')

model.summary()

from keras import models
from keras import layers
from tensorflow.keras import optimizers

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(learning_rate=1e-4),
              metrics=['acc'])

img = cv2.imread('/content/drive/MyDrive/Leaf/Test/Akapulko/IMG20220428082202.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img,(224,224))
imgs = np.reshape(img,[1,224,224,3])

classes_x=model.predict(imgs)
prediction=np.argmax(classes_x,axis=1)

labels = np.array(['Akapulko', 'Aloe Vera', 'Ampalaya', 'Bayabas', 'Guyabano', 'Katakataka', 'Kusay',
   'Lagundi', 'Luya', 'Malunggay', 'Oregano', 'Pansit-pansitan', 'Paragis'])
labels = labels.reshape(labels.shape,)
print(labels)

akapulko = """      Akapulko is a tradional herbal medicine and is a shrub that grows wild in tropical climates such as the Philippines.

Akapulko is traditionally used to treat the following:
>>> Tinea infections
>>> Insect bites
>>> Ringworms
>>> Eczema
>>> Scabies
>>> Itchiness

Preparation and usage of Akapulko
Pound Akapulko leaves, squeeze the juice and apply topically on affected area twice a day until cured. There are commercially available
Akapulko herbal medicine lotions in the Philippine market for skin diseases treatment. If symptoms persist or irritation occurs, stop the
use and consult your doctor."""

aloevera = """     Aloe vera is one of the oldest known herbal medicine that can be traced back in ancient Egypt. Aloe Vera is a herb
that grows in warm climates and is widely distributed in the Philippines.

Aloe Vera is traditionally used to treat the following:
>>> Dandruff
>>> Thinning and falling hair
>>> Baldness

Preparation and usage of Aloe Vera
Fresh Aloe Vera juice or sap are massaged to the affected scalp and let it stay for a few minutes before washing."""

ampalaya = """      Ampalaya or bitter melon also known as bitter gourd as the name implies has a bitter taste due to the presence of
momordicin. Ampalaya is a tropical and subtropical vine of the family Cucurbitaceae, widely grown in the Philippines for its edible fruit.

Ampalaya or bitter gourd is a widely used herbal remedy to lower the blood sugar levels for diabetic patients.

Preparation and usage of Ampalaya
Green fruit and young leaves of Ampalaya are cooked mixed with meat. To lessen the bitterness of the ampalaya fruit, wash or even boiled in
water with salt."""

bayabas = """       Bayabas or guava fruit is known for being rich in vitamin C and vitamin A. It is a fruit bearing shrub or small tree
that grows in the tropical climate like Philippines.

Bayabas is traditionally used to treat the following:
>>> Antiseptic
>>> Anti-inflammatory
>>> Anti-spasmodic
>>> Antioxidant
>>> Anti-allergy
>>> Antimicrobial
>>> Anti-plasmodial
>>> Anti-cough
>>> Antidiabetic
>>> Antigenotoxic
>>> Hepatoprotective

Preparation and usage of Bayabas
Gather fresh bayabas leaves and wash with water.
Boil one cup of bayabas leaves in three cups of water for 8 to 10 minutes.
Strain and let cool.
To use as wound disinfectant, wash affected areas 2 to 3 times a day.
Fresh bayabas leaves can also be chewed for the treatment of toothache and gum swelling.
To hasten wound healing, fresh bayabas leaf poultice may be applied to the wound."""

guyabano = """      Guyabano is a fruit bearing tree, broadleaf, flowering, and evergreen.  Guyabano or Soursop is adaptable to tropical
climate and are currently cultivated for its fruit.

Guyabano is traditionally used to treat the following:
>>> It helps lower fever, spasms, heart rate, and blood pressure
>>> It also helps relieve pain, inflammation, and asthma.

Preparation and usage of Guyabano
10 leaves of guyabano,
Boil the guyabano leaves in the water
Simmer for 20 minutes
Strain and let cool
Ready for drink"""

katakataka = """"     Katakataka is a succulent perennial plant that is commonly used to treat wounds and minor illnesses. Medicinal
uses have been recognized in the herbal medicine industry for many years now.

Katakataka is traditionally used to treat the following:
>>> Cough
>>> Arthritis
>>> Hypertension
>>> Headaches

Preparation and usage of Katakataka
For relief of eye styes, heat the katakataka leaf and place it over the affected eye area for 1 minute at least 3 times every day.
For headache relief, heat katakataka leaves and place on your forehead for around 10 minutes.
To relieve backache or joint pains, heat the leaves and place them on the affected area until the throbbing or aching is alleviated.
In treating sprains, burns and infections, pound fresh katakataka leaves and apply to the affected area.
With its antiviral characteristics, Katakataka leaves are sometimes boiled to make a warm drink for those with flu or colds.
For sore feet, soak your feet in warm water with katakataka leaves."""

kusay = """     Kusay is a perennial plant that grows in clumps just like the lilies. It produces many white flowers in a round
cluste. It grows in slowly expanding perennial clumps, but also readily sprouts from seed.

Kusay is traditionally used to treat 	bruises

Preparation and usage of Kusay
Pound enough leaves.
Squeeze out the juice.
Rub juice on affected part."""

lagundi = """     Lagundi is a large native shrub that grows in Asia and Southeast Asia such as the Philippines and India and has
been traditionally used as herbal medicine.

Lagundi is traditionally used to treat the following:
>>> Asthma
>>> Cough
>>> Colds
>>> Fever

Preparation and usage of Lagundi
Mix one cup of cut fresh leaves to 2 cups of water.
Boil for 10 minutes.
Let it steep and strain the solid parts.
Take 1/2 cup, three times a day until condition improve."""

luya = """      Luya has been used as a medicine for hundred of years, and is one of the earliest documented herbs utilized for the
maintenance of health and treatment of disease.

Luya is traditionally used to treat the following:
>>> Antibacterial
>>> Anti- inflamatory
>>> Anti nausea
>>> Treatment of sore throat.

Preparation and usage of Luya
Prepare by chopping luya or ginger (200 grms - dried or 300 grams - fresh) for every liter of desired preparation.
You may use as preparation vinegar, glycerol, distilled water or rum for alcohol based tincture (never use isopropyl, rubbing
or any industrial grade alcohol)
Mix the luya or ginger with your preparation in a sterilized glass jar and seal it properly.
Keep the jar in a dark area for about 2 weeks, shaking the glass jar every day.
Filter with cheesecloth the luya or ginger liquid and transfer the tincture in a colored glass container.
Luya or ginger tincture may be taken 1 teaspoon 1- 3 times a day. diluted as tea or juice."""

malunggay = """     Malunggay is a popular plant known for high nutritional value as well as an herbal medicine. Malunggay is a plant
that grows in the tropical climates such as the Philippines. It is widely used as herbal medicine for a number of illness and other
practical uses.

Malunggay is traditionally used to treat the following:
>>> Combat malnutrition
>>> Boosts immune system
>>> Milk production in nursing mothers

Preparation and usage of Malunggay
Pick out 4 to 5 branches from the tree. Choose those with lots of leaves.
Place them on a tray and leave in a dry place anywhere in your home for 3-4 days or until the leaves dry up and become crumpled.
Pick out the crumpled leaves from the twigs and place in a dry pan over a low fire. Do not place water or oil in the pan.
Cook the leaves, turning them over with a cooking spoon so that the leaves are cooked evenly. They are cooked when they are toasted
but not burned.
Store the cooked leaves in any container with a cover.
To make the tea, take a tablespoon of the cooked leaves from the container and place in a cup of hot water. Let sit until the water
absorbs the green color and nutrients of the leaves. It takes the same amount of time as making ordinary tea from tea bags.
Remove the leaves from the cup.
Option: add honey."""

oregano = """     Oregano is considered as a perennial plant that grows in warm temperate areas. oregano has established itself in folkloric medicine.

Oregano is traditionally used to treat the following:
>>> Sore throat
>>> Asthma
>>> Colds
>>> Coughs
>>> Flu

Preparation and usage of Oregano
Chop fresh oregano leaves
Add 1 tablespoon for every cup of water
Boil for 15 to 20 minutes
Let it steep then strain
Take one cup once a day until condition improves"""

pansitpansitan = """     Pansit-pansitan is a common fleshy shallow rooted herb that has been used as a medicinal herb.
Pansit-pansitan has taken its niche in the folkloric herbal medicine providing health benefits.

Pansit-pansitan is traditionally used to treat the following:
>>> Gout
>>> Arthritis

Preparation and usage of Pansit=pansitan
Wash freshly gathered pansit-pansitan leaves
Chop then add in 4 cups of water for every 1 cup
Let it boil for 10 to 15 minutes with the pot cover removed
Let it steep then strain
Drink half cup of Pansit-pansitan tea three times a day"""

paragis = """     Paragis is an erect, tufted, and glabrous grass with long and tapered leaves. It can grow between 10 centimeters
and 1 meter in height.

Pansit-pansitan is traditionally used to treat the following:
>>> Diabetes
>>> High blood pressure
>>> Ovarian cyst
>>> Myoma

Preparation and usage of Paragis
Boil a bunch of the weed in one liter of water for 10-15 minutes.
Then drink it hot, lukewarm, or cold, depending on personal choice."""

plt.imshow(img)
print(colored(labels[prediction], 'red'))
if prediction == 0:
  print(colored(akapulko, 'green'))
elif prediction == 1:
  print(colored(aloevera, 'green'))
elif prediction == 2:
  print(colored(ampalaya, 'green'))
elif prediction == 3:
  print(colored(bayabas, 'green'))
elif prediction == 4:
  print(colored(guyabano, 'green'))
elif prediction == 5:
  print(colored(katakataka, 'green'))
elif prediction == 6:
  print(colored(kusay, 'green'))
elif prediction == 7:
  print(colored(lagundi, 'green'))
elif prediction == 8:
  print(colored(luya, 'green'))
elif prediction == 9:
  print(colored(malunggay, 'green'))
elif prediction == 10:
  print(colored(oregano, 'green'))
elif prediction == 11:
  print(colored(pansitpansitan, 'green'))
elif prediction == 12:
  print(colored(paragis, 'green'))

"""# **Confusion Matrix**

"""

from keras.models import load_model

model = load_model('/content/drive/MyDrive/Leaf/leafvgg19.h5')

from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np

test_dir = '/content/drive/MyDrive/New2/test'

test_datagen = ImageDataGenerator()

test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(224, 224),
        batch_size=30,
        class_mode='categorical',
        shuffle= False)

y_pred=model.predict(test_generator)
predict=np.argmax(y_pred, axis=1)

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):

    plt.figure(figsize=(20,20))

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm = np.around(cm, decimals=2)
        cm[np.isnan(cm)] = 0.0
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
   # plt.savefig('/content/drive/MyDrive/Leaves/ConfusionMatrix.png')

from sklearn.metrics import classification_report, confusion_matrix
import itertools

target_names = []
for key in test_generator.class_indices:
    target_names.append(key)

print('Confusion Matrix')
cm = confusion_matrix(test_generator.classes, predict)
plot_confusion_matrix(cm, target_names, title='Confusion Matrix')

print('Classification Report')
print(classification_report(test_generator.classes, predict, target_names=target_names))