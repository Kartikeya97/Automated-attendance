import pymysql.cursors  
import csv

class DatabaseInitializer:

    def __init__(self):
        self.connection = 0


    def ReadCSVRollList(self, file_name):
        roll_list = []

        # Opening and reading CSV File
        with open(file_name, newline='') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

            # Creating a Roll List(Roll Number and Name)
            for row in file_reader:
                roll_list.append(row)
                
        return roll_list
    
                
    def EC_MySQLServer(self, host, user, password, port):
        msg = ""
        # Connecting to MYSQL Server
        try:
            self.connection = pymysql.connect(host = host, user = user, password = password, port = port, cursorclass = pymysql.cursors.DictCursor)
            msg = "Connection Successfully Established with MySQL Server!"
        except Exception:
            msg = "Unnable to Connect with MySQL Server!"

        return msg
        
        
    def EC_Database(self, host, user, password, port, db_name):
        msg = ""
        try:
            self.connection = pymysql.connect(host = host, user = user, password = password, port = port, database = db_name, cursorclass = pymysql.cursors.DictCursor)
            msg = "Connection Successfully Established with the Database!"
        except Exception:
            msg = "Unnable to Connect with the Databse!"
            
        return msg
    
    
    def CreateDatabase(self, db_name):
        msg = ""
        # Query for Creating Database
        query = "CREATE DATABASE " + db_name

        # Creating Database 
        try: 
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                msg = "DataBase successfully created!"
        except Exception:
                msg = "Unnable to create the database!"
                
        return msg
    
    
    def CreateTable(self, table_name):
        msg = ""
        # Query for Creating Table
        query = "CREATE TABLE " + str(table_name) + " (S_No INT(1) NOT NULL AUTO_INCREMENT, Roll_No INT(1) NOT NULL, Name VARCHAR(35) NOT NULL, Day_1 CHAR(1) NULL, Day_2 CHAR(1) NULL, Day_3 CHAR(1) NULL, Day_4 CHAR(1) NULL, Day_5 CHAR(1) NULL, Day_6 CHAR(1) NULL, Day_7 CHAR(1) NULL, Day_8 CHAR(1) NULL, Day_9 CHAR(1) NULL, Day_10 CHAR(1) NULL, Day_11 CHAR(1) NULL, Day_12 CHAR(1) NULL, Day_13 CHAR(1) NULL, Day_14 CHAR(1) NULL, Day_15 CHAR(1) NULL, Day_16 CHAR(1) NULL, Day_17 CHAR(1) NULL, Day_18 CHAR(1) NULL, Day_19 CHAR(1) NULL, Day_20 CHAR(1) NULL, Day_21 CHAR(1) NULL, Day_22 CHAR(1) NULL, Day_23 CHAR(1) NULL, Day_24 CHAR(1) NULL, Day_25 CHAR(1) NULL, Day_26 CHAR(1) NULL, Day_27 CHAR(1) NULL, Day_28 CHAR(1) NULL, Day_29 CHAR(1) NULL, Day_30 CHAR(1) NULL, Day_31 CHAR(1) NULL, PRIMARY KEY(S_No));"

        # Creating Table
        try: 
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                msg = "Table Created Successfully!"

        except Exception:
           msg = "Unable to create the table!"

        return msg


    def InitializeTable(self, table_name, roll_list):
        flag = 0
        # Looping through the Roll List
        for roll_no, name in roll_list:
            # Query to initialize table with roll_list
            query = "INSERT INTO " + str(table_name) + " (Roll_No, Name) VALUES('" + str(roll_no) + "', '" + (name) + "');"           

            # Executing query to initialize table with roll_list
            try: 
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    self.connection.autocommit(True)
            except Exception:
                flag = 1    
                    
        if (flag == 0):
            msg = "Table Initialized Successfully!"
        else:
            msg = "Unnable to initialize the table!"
            
        return msg


    def DisconnectDatabase(self):
        # Disconnecting Database
        if(self.connection != 0):
            self.connection.close()

            self.connection = 0
            print("Database Disconnected!")
        



DI = DatabaseInitializer()
roll_list = DI.ReadCSVRollList("DatabaseEntities/RollList.csv")

host = 'localhost'
user = 'root'
password = ''
port = 3306
db_name = 'attendance'
table_name = 'subject'
'''
print(DI.EC_MySQLServer(host, user, password, port))
print(DI.CreateDatabase(db_name))
print(DI.EC_Database(host, user, password, port, db_name))
print(DI.CreateTable(table_name))
print(DI.InitializeTable(table_name, roll_list))
'''
DI.DisconnectDatabase()