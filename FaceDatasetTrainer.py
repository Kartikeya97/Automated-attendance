import os, sys
sys.path.append(os.path.abspath(__file__))

import keras
from keras.models import Model
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator


class FaceDatasetTrainer:
    def __init__(self):
        # Setting Dataset paths
        self.train_path = 'Dataset/TrainingDataSet/TrainingImages/'
        self.validate_path = 'DataSet/TrainingDataSet/ValidationImages/'
        
        self.no_of_classes = 4      
    
    
    def ParameterPreparation(self):
        # Creating class list labels
        self.class_list = []
        for i in range(0, self.no_of_classes):
            self.class_list.append(str(i))
        
        # Creating training and validation image batches
        self.train_batches = ImageDataGenerator().flow_from_directory(self.train_path, target_size=(224,224), classes=self.class_list, batch_size=10)
        self.validate_batches = ImageDataGenerator().flow_from_directory(self.validate_path, target_size=(224,224), classes=self.class_list, batch_size=5)


    # Function to generate custom VGG
    def GenerateVGG16Model(self):
        # Generate a model with all layers (with top)
        vgg16 = keras.applications.vgg16.VGG16(weights=None, include_top=True)
        #Add a layer where input is the output of the  second last layer
        x = Dense(4, activation='softmax', name='predictions')(vgg16.layers[-2].output)
        # Then create the corresponding model
        self.custom_vgg16_model = Model(input=vgg16.input, output=x)
        # Compiling the custom VGG16 model
        self.custom_vgg16_model.compile(Adam(lr=.0001), loss='categorical_crossentropy', metrics=['accuracy'])    
    

    def Trainer(self):
        # Preparing some parameters before training the model
        self.ParameterPreparation()
        # Building the custom VGG16 model
        self.GenerateVGG16Model()

        print("Training Started...")
        # Training and Validating the custom VGG16 model with the images
        self.custom_vgg16_model.fit_generator(self.train_batches, steps_per_epoch=10, validation_data=self.validate_batches, validation_steps=10, epochs=1, verbose=2)
        print("Training Successfully Completed!")                

        # Serializing modal to YAML
        self.custom_vgg16_model_yaml = self.custom_vgg16_model.to_yaml()
        with open("TrainedEntities/custom_vgg16_model.yaml", "w") as yaml_file:
            yaml_file.write(self.custom_vgg16_model_yaml)            

        # Serializing weights to HDF5
        self.custom_vgg16_model.save_weights("TrainedEntities/custom_vgg16_model_weights.h5")
        print("Modal saved to disk")
        
        
        
def main():
    # Creating object of the class
    FDT = FaceDatasetTrainer()

    # Detecting the faces in the frame
    FDT.Trainer()


if __name__ == "__main__":
    main()