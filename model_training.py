from keras_vggface.vggface import VGGFace
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Flatten
from keras.models import Model

# Load pre-trained VGGFace model
base_model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

# Adding custom layers for retraining
x = base_model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Data Augmentation for training with new data
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8,1.2])

# Load your dataset (make sure to organize your dataset in the correct directory structure)
train_generator = train_datagen.flow_from_directory(
    'path_to_missing_children_dataset',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary')

# Train the model
model.fit(train_generator, epochs=10)

# Save the trained model
model.save('missing_children_model.h5')
