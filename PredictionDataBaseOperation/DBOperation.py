import shutil
import sqlite3
from os import listdir
import os
import csv
from logger import App_Logger


class dBOperation:
    """
          This class shall be used for handling all the SQL operations.

          Written By: Durgesh Kumar
          Version: 1.0
          Revisions: None

          """

    def __init__(self):
        self.path = 'PredictionDatabase/'
        self.badFilePath = "PredictionRawFilesValidated/BadRaw"
        self.goodFilePath = "PredictionRawFilesValidated/GoodRaw"
        self.logger = App_Logger()

    def dataBaseConnection(self,DatabaseName):

        """
                        Method Name: dataBaseConnection
                        Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                        Output: Connection to the DB
                        On Failure: Raise ConnectionError

                         Written By: Durgesh Kumar
                        Version: 1.0
                        Revisions: None

                        """
        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')

            file = open("PredictionLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()
        except ConnectionError:
            file = open("PredictionLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn


    def createTableDb(self,DatabaseName,column_names):

        """
           Method Name: createTableDb
           Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
           Output: None
           On Failure: Raise Exception

            Written By: Durgesh Kumar
           Version: 1.0
           Revisions: None

        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            conn.execute('DROP TABLE IF EXISTS GoodRawData;')

            for key in column_names.keys():
                type = column_names[key]

                # we will remove the column of string datatype before loading as it is not needed for training
                #in try block we check if the table exists, if yes then add columns to the table
                # else in catch block we create the table
                try:
                    #cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                    conn.execute('ALTER TABLE GoodRawData ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                except:
                    conn.execute('CREATE TABLE  GoodRawData ({column_name} {dataType})'.format(column_name=key, dataType=type))

            conn.close()

            file = open("PredictionLog/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Tables created successfully!!")
            file.close()

            file = open("PredictionLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()


        except Exception as e:
            file = open("PredictionLog/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("PredictionLog/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e


    def insertIntoTableGoodData(self,Database):

        """
                                       Method Name: insertIntoTableGoodData
                                       Description: This method inserts the Good data files from the Good_Raw folder into the
                                                    above created table.
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: Durgesh Kumar
                                       Version: 1.0
                                       Revisions: None

                """

        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        file = open("PredictionLog/DbInsertLog.txt", 'a+')

        for files in onlyfiles:
            try:

                with open(goodFilePath+'/'+files, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO GoodRawData values ({values})'.format(values=(list_)))
                                self.logger.log(file," %s: File loaded successfully!!" % files)
                                conn.commit()
                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                self.logger.log(file,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + files, badFilePath)
                self.logger.log(file, "File Moved Successfully %s" % files)
                file.close()
                conn.close()
                raise e

        conn.close()
        file.close()


    def selectingDatafromtableintocsv(self,Database):

        """
                                       Method Name: selectingDatafromtableintocsv
                                       Description: This method exports the data in GoodData table as a CSV file. in a given location.
                                                    above created .
                                       Output: None
                                       On Failure: Raise Exception

                                        Written By: Durgesh Kumar
                                       Version: 1.0
                                       Revisions: None

                """

        self.fileFromDb = 'PredictionFileFromDB/'
        self.fileName = 'InputFile.csv'
        log_file = open("PredictionLog/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM GoodRawData"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            #Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            raise e