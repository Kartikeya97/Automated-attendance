import os, sys
sys.path.append(os.path.abspath(__file__))
import pymysql.cursors
import datetime


class DatabaseUpdater:

    def __init__(self):
        self.connection = 0        
        
        
    def EC_Database(self, host, user, password, port, db_name):
        msg = ""
        try:
            self.connection = pymysql.connect(host = host, user = user, password = password, port = port, database = db_name, cursorclass = pymysql.cursors.DictCursor)
            msg = "Connection Successfully Established with the Database!"
        except Exception:
            msg = "Unnable to Connect with the Databse!"
            
        return msg
        
    
    def GetRollNos_Database(self, table_name):
        msg = ""
        # Query to get roll numbers form databse
        query = "SELECT Roll_No, Name FROM " + table_name + ";"

        # Executing query to get roll numbers form databse           
        try: 
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                # Fetching all the roll numbers from the database
                roll_list =  cursor.fetchall()
                
                return roll_list
        except Exception:
            msg = "Unable to get the roll numbers!"
            
        return msg


    def ValidateRollNumber(self, predicted_roll_ids, roll_list):      
        validated_names = []
        # Looping through predicted_roll_ids with database roll_list to validate predicted_roll_ids
        for roll_id in predicted_roll_ids:
            for row in roll_list:
                # Returning name if predicted roll number exists in roll list
                if(row['Roll_No'] == roll_id):
                    validated_names.append(row['Name'])
            
        # Returning -1 if predicted roll numbers are not present database roll_list
        if(len(validated_names) == 0):
            return -1
        else:
            return validated_names


    def UpdateDatabase(self, table_name, predicted_roll_ids):
        flag = 0
        # Calculating current date(dd)
        now = datetime.datetime.now()
        day = "%d" % now.day

        for roll_id in predicted_roll_ids:
            # Query for updating attendance 
            query = "UPDATE " + table_name + " SET Day_" + day + " = 'P' WHERE Roll_No = " + str(roll_id) + ";"

            # Executing query for updating attendance
            try: 
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    # Committing for updation
                    self.connection.autocommit(True)
            except Exception:
                flag = 1
                
                
        if (flag == 0):
            msg = "Database Updated Successfully"
        else:
            msg = "Unable to update the database!"
        
        return msg


    def DisconnectDatabase(self):
        msg = ""
        # Disconnecting database
        if(self.connection != 0):
            self.connection.close()

            self.connection = 0
            msg = "Database Disconnected!"
        
        return msg
        

        
        




