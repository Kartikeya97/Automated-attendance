import os, sys
sys.path.append(os.path.abspath(__file__))

from FacePredictor import *
from DatabaseUpdater import *

class PU_Driver:
    
    def __init__(self):        
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.port = 3306
        self.db_name = 'attendance'
        self.table_name = 'subject'
        self.predicted_roll_ids = []
        
        self.session_img_path = "Dataset/RawImages/"
        
        # Creating object for class 'FaceDetectorPredictor'
        self.FDP = FacePredictor() 
        # Creating object for class 'DatabaseUpdater'
        self.DU = DatabaseUpdater()
        
        
    def RunPredictor(self, test_image):
        # Predicting the faces of test image dataset
        roll_list = self.FDP.Predictor(test_image)
        self.predicted_roll_ids += roll_list            
    
    
    def RunUpdater(self):
        self.DU.EC_Database(self.host, self.user, self.password, self.port, self.db_name)
        self.roll_list = self.DU.GetRollNos_Database(self.table_name)
        names = self.DU.ValidateRollNumber(self.predicted_roll_ids, self.roll_list)
        self.DU.UpdateDatabase(self.table_name, self.predicted_roll_ids)
        self.DU.DisconnectDatabase()
        
        return names
    
    def SessionImageLoader(self):
        # Looping to find the uploading images
        for file in os.listdir(self.session_img_path):
            self.RunPredictor(self.session_img_path + file)
        
        # Creating list of unique Ids
        self.predicted_roll_ids = list(set(self.predicted_roll_ids))
        
        # Updating Database with the predicted Roll_Ids
        return self.RunUpdater()
            

    
PUD = PU_Driver()
print(PUD.SessionImageLoader())
