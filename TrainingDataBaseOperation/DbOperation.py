import sqlite3
import shutil
from datetime import datetime
import os
from os import listdir
import csv
from logger import App_Logger


class DbOperation:
    """
      This class shall be used for handling all the SQL operations and Data Type Validation.

      Written By: Durgesh Kumar
      Version: 1.0
      Revisions: None

      """
    def __init__(self):
        self.path = 'TrainingDataBase/'
        self.BadFilesPath = "TrainingRawValidatedFiles/BadRaw"
        self.GoodFilesPath = "TrainingRawValidatedFiles/GoodRaw"
        self.logger = App_Logger()


    def DataBaseConnection(self, DataBaseName):

        """
                Method Name: DataBaseConnection
                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                Output: Connection to the DB
                On Failure: Raise ConnectionError

                 Written By: Durgesh Kumar
                Version: 1.0
                Revisions: None

        """

        try:
            conn = sqlite3.connect(self.path+DataBaseName+'.db')
            file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s DataBase Successfully" %DataBaseName)
            file.close()

        except ConnectionError:
            file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error While connecting to Database : %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn



    def CreateTableInDB(self,DataBaseName,ColumnName):
        """
                        Method Name: CreateTableInDB
                        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
                        Output: None
                        On Failure: Raise Exception

                         Written By: Durgesh Kumar
                        Version: 1.0
                        Revisions: None

        """
        try:
            conn = self.DataBaseConnection(DataBaseName)
            c = conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'GoodRawData'")
            if c.fetchone()[0] == 1:
                conn.close()
                file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Tables Created Successfully!!!")
                file.close()

                file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database Successfully!!" %DataBaseName)
                file.close()

            else:
                for key in ColumnName.keys():
                    type = ColumnName[key]

                    # in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table

                    try:
                        # cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='GoodRawData'".format(dbName=DatabaseName))
                        conn.execute('ALTER TABLE GoodRawData ADD COLUMN "{ColumnName}" {dataType}'.format(ColumnName =key, dataType=type))
                    except:
                        conn.execute('CREATE TABLE GoodRawData ({ColumnName} {dataType})'.format(ColumnName =key, dataType=type))

                conn.close()
                file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" %DataBaseName)
                file.close()


        except Exception as e:
            file = open ("TrainingLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error While Creating table: %s" %e)
            file.close()
            conn.close()
            file = open("TrainingLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s DataBase Successfully!!!" %DataBaseName)
            file.close()
            raise e




    def InsertGoodDataIntoTable(self,DataBase):

        """
                                       Method Name: InsertGoodDataIntoTable
                                       Description: This method inserts the Good data files from the Good_Raw folder into the
                                                    above created table.
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: Durgesh Kumar
                                       Version: 1.0
                                       Revisions: None

                """

        conn = self.DataBaseConnection(DataBase)
        GoodFilesPath = self.GoodFilesPath
        BadFilesPath = self.BadFilesPath
        OnlyFiles = [f for f in listdir(GoodFilesPath)]
        file = open("TrainingLog/DBInsertLog.txt", 'a+')

        for files in OnlyFiles:
            try:
                with open(GoodFilesPath + '/' + files, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO GoodRawData values ({values})'.format(values=(list_)))
                                self.logger.log(file,"%s: File Loaded Successfully!!!" %files)
                                conn.commit()
                            except Exception as e:
                                raise e


            except Exception as e:
                conn.rollback()
                self.logger.log(file, "Error While Creating table: %s" %e)
                shutil.move(GoodFilesPath+'/'+files, BadFilesPath)
                self.logger.log(file, "File Moved Successfully : %s" %files)
                file.close()
                conn.close()

        conn.close()
        file.close()



    def SelectingDataFromTableIntoCsv(self,DataBase):
        """
                                       Method Name: SelectingDataFromTableIntoCsv
                                       Description: This method exports the data in GoodRawData table as a CSV file. in a given location.
                                                    above created .
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: Durgesh Kumar
                                       Version: 1.0
                                       Revisions: None

        """


        self.FileFromDB = 'TraingingFilesFromDB/'
        self.FileName = "InputFile.csv"
        file = open("TrainingLog/ExportToCsvLog.txt", 'a+')

        try:
            conn = self.DataBaseConnection(DataBase)
            SqlSelect = "SELECT * FROM GoodRawData"
            cursor = conn.cursor()
            cursor.execute(SqlSelect)
            result = cursor.fetchall()

            # Get the headers of the Csv Files
            headers = [i[0] for i in cursor.description]

            # Make the CSV Output Directory
            if not os.path.isdir(self.FileFromDB):
                os.makedirs(self.FileFromDB)

            #Open CSV File for writing
            CsvFile = csv.writer(open(self.FileFromDB + self.FileName, 'w' , newline='') , delimiter = ',' , lineterminator = '\r\n' , quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the header and data To Csv FIle
            CsvFile.writerow(headers)
            CsvFile.writerows(result)

            self.logger.log(file , "File Exported Successfully!!!!")
            file.close()

        except Exception as e:
            self.logger.log(file , "File Exported Failed. Error : %s" %e)
            file.close()



























