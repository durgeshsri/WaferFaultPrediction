import sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
from logger import App_Logger

class PredictionDataValidation:
    """
    This class shall be used for handling all the validation done on the Raw Prediction Data!!.

    Written By: Durgesh Kumar
    Version: 1.0
    Revisions: None

    """

    def __init__(self,path):
        self.BatchDirectory = path
        self.SchemaPath = 'schema_prediction.json'
        self.logger = App_Logger()


    def valuesFromSchema(self):
        """
                                Method Name: valuesFromSchema
                                Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                                Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                                On Failure: Raise ValueError,KeyError,Exception

                                 Written By: Durgesh Kumar
                                Version: 1.0
                                Revisions: None

        """

        try:
            with open(self.SchemaPath, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            ColumnNames = dic['ColName']
            NumberOfColumns = dic['NumberofColumns']

            file = open("PredictionLog/ValuesfromSchemaValidationLog.txt", 'a+')
            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberOfColumns + "\n"
            self.logger.log(file,message)

            file.close()



        except ValueError:
            file = open("PredictionLog/ValuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema.json")
            file.close()
            raise ValueError

        except KeyError:
            file = open("PredictionLog/ValuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("PredictionLog/ValuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, ColumnNames, NumberOfColumns



    def ManualRegexCreation(self):

        """
                                      Method Name: ManualRegexCreation
                                      Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                                  This Regex is used to validate the filename of the prediction data.
                                      Output: Regex pattern
                                      On Failure: None

                                       Written By: Durgesh Kumar
                                      Version: 1.0
                                      Revisions: None

        """
        regex = "['wafer']+['\_'']+[\d_]+[\d]+\.csv"
        return regex


    def CreateDirectoryForGoodBadRawData(self):

        """
                                        Method Name: CreateDirectoryForGoodBadRawData
                                        Description: This method creates directories to store the Good Data and Bad Data
                                                      after validating the prediction data.

                                        Output: None
                                        On Failure: OSError

                                         Written By: Durgesh Kumar
                                        Version: 1.0
                                        Revisions: None

                """
        try:
            path = os.path.join("PredictionRawFilesValidated/", "GoodRaw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("PredictionRawFilesValidated/", "BadRaw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:
            file = open("PredictionLog/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" % ex)
            file.close()
            raise OSError


    def DeleteExistingGoodDataTrainingFolder(self):
        """
                                            Method Name: DeleteExistingGoodDataTrainingFolder
                                            Description: This method deletes the directory made to store the Good Data
                                                          after loading the data in the table. Once the good files are
                                                          loaded in the DB,deleting the directory ensures space optimization.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Durgesh Kumar
                                            Version: 1.0
                                            Revisions: None

                                                    """
        try:
            path = 'PredictionRawFilesValidated/'
            if os.path.isdir(path + 'GoodRaw/'):
                shutil.rmtree(path + 'GoodRaw/')
                file = open("PredictionLog/GeneralLog.txt", 'a+')
                self.logger.log(file,"GoodRaw directory deleted successfully!!!")
                file.close()
        except OSError as s:
            file = open("PredictionLog/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError

    def DeleteExistingBadDataTrainingFolder(self):

        """
                                            Method Name: DeleteExistingBadDataTrainingFolder
                                            Description: This method deletes the directory made to store the bad Data.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Durgesh Kumar
                                            Version: 1.0
                                            Revisions: None

                                                    """

        try:
            path = 'PredictionRawFilesValidated/'
            if os.path.isdir(path + 'BadRaw/'):
                shutil.rmtree(path + 'BadRaw/')
                file = open("PredictionLog/GeneralLog.txt", 'a+')
                self.logger.log(file,"BadRaw directory deleted before starting validation!!!")
                file.close()
        except OSError as s:
            file = open("PredictionLog/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while Deleting Directory : %s" %s)
            file.close()
            raise OSError



    def MoveBadFilesToArchiveBad(self):


        """
                                            Method Name: MoveBadFilesToArchiveBad
                                            Description: This method deletes the directory made  to store the Bad Data
                                                          after moving the data in an archive folder. We archive the bad
                                                          files to send them back to the client for invalid data issue.
                                            Output: None
                                            On Failure: OSError

                                             Written By: Durgesh Kumar
                                            Version: 1.0
                                            Revisions: None

                                                    """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:
            path= "PredictionArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)
            source = 'PredictionRawFilesValidated/BadRaw/'
            dest = 'PredictionArchivedBadData/BadData_' + str(date)+"_"+str(time)
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + f, dest)
            file = open("PredictionLog/GeneralLog.txt", 'a+')
            self.logger.log(file,"Bad files moved to archive")
            path = 'PredictionRawFilesValidated/'
            if os.path.isdir(path + 'BadRaw/'):
                shutil.rmtree(path + 'BadRaw/')
            self.logger.log(file,"Bad Raw Data Folder Deleted successfully!!")
            file.close()
        except OSError as e:
            file = open("Prediction_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)
            file.close()
            raise OSError



    def ValidationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
            Method Name: ValidationFileNameRaw
            Description: This function validates the name of the prediction csv file as per given name in the schema!
                         Regex pattern is used to do the validation.If name format do not match the file is moved
                         to Bad Raw Data folder else in Good raw data.
            Output: None
            On Failure: Exception

             Written By: Durgesh Kumar
            Version: 1.0
            Revisions: None

        """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.DeleteExistingBadDataTrainingFolder()
        self.DeleteExistingGoodDataTrainingFolder()
        self.CreateDirectoryForGoodBadRawData()
        onlyfiles = [f for f in listdir(self.BatchDirectory)]
        try:
            file = open("PredictionLog/NameValidationLog.txt", 'a+')
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if len(splitAtDot[1]) == LengthOfDateStampInFile:
                        if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                            shutil.copy("PredictionBatchfiles/" + filename, "PredictionRawFilesValidated/GoodRaw")
                            self.logger.log(file,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy("PredictionBatchfiles/" + filename, "Prediction_Raw_Files_Validated/BadRaw")
                            self.logger.log(file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy("PredictionBatchfiles/" + filename, "PredictionRawFilesValidated/BadRaw")
                        self.logger.log(file,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy("PredictionBatchfiles/" + filename, "PredictionRawFilesValidated/BadRaw")
                    self.logger.log(file, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            file.close()

        except Exception as e:
            file = open("PredictionLog/NameValidationLog.txt", 'a+')
            self.logger.log(file, "Error occured while validating FileName %s" % e)
            file.close()
            raise e


    def ValidateColumnLength(self,NumberofColumns):
        """
                    Method Name: ValidateColumnLength
                    Description: This function validates the number of columns in the csv files.
                                 It is should be same as given in the schema file.
                                 If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                                 If the column number matches, file is kept in Good Raw Data for processing.
                                The csv file is missing the first column name, this function changes the missing name to "Wafer".
                    Output: None
                    On Failure: Exception

                     Written By: Durgesh Kumar
                    Version: 1.0
                    Revisions: None

             """
        try:
            file = open("PredictionLog/ColumnValidationLog.txt", 'a+')
            self.logger.log(file,"Column Length Validation Started!!")
            for files in listdir('PredictionRawFilesValidated/GoodRaw/'):
                csv = pd.read_csv("PredictionRawFilesValidated/GoodRaw/" + files)
                if csv.shape[1] == NumberofColumns:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("PredictionRawFilesValidated/GoodRaw/" + files, index=None, header=True)
                else:
                    shutil.move("PredictionRawFilesValidated/GoodRaw/" + files, "PredictionRawFilesValidated/BadRaw")
                    self.logger.log(file, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % files)

            self.logger.log(file, "Column Length Validation Completed!!")
        except OSError:
            file = open("Prediction_Logs/ColumnValidationLog.txt", 'a+')
            self.logger.log(file, "Error Occured while moving the file :: %s" % OSError)
            file.close()
            raise OSError
        except Exception as e:
            file = open("Prediction_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(file, "Error Occured:: %s" % e)
            file.close()
            raise e

        file.close()

    def DeletePredictionFile(self):

        if os.path.exists('PredictionOutputFile/Predictions.csv'):
            os.remove('PredictionOutputFile/Predictions.csv')


    def ValidateMissingValuesInWholeColumn(self):
        """
                                  Method Name: ValidateMissingValuesInWholeColumn
                                  Description: This function validates if any column in the csv file has all values missing.
                                               If all the values are missing, the file is not suitable for processing.
                                               SUch files are moved to bad raw data.
                                  Output: None
                                  On Failure: Exception

                                   Written By: Durgesh Kumar
                                  Version: 1.0
                                  Revisions: None

                              """
        try:
            file = open("PredictionLog/MissingValuesInColumn.txt", 'a+')
            self.logger.log(file, "Missing Values Validation Started!!")

            for files in listdir('PredictionRawFilesValidated/GoodRaw/'):
                csv = pd.read_csv("PredictionRawFilesValidated/GoodRaw/" + files)
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("PredictionRawFilesValidated/GoodRaw/" + files,"PredictionRawFilesValidated/BadRaw")
                        self.logger.log(file,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % files)
                        break
                if count==0:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv("PredictionRawFilesValidated/GoodRaw/" + files, index=None, header=True)
        except OSError:
            file = open("PredictionLog/MissingValuesInColumn.txt", 'a+')
            self.logger.log(file, "Error Occured while moving the file :: %s" % OSError)
            file.close()
            raise OSError
        except Exception as e:
            file = open("PredictionLog/MissingValuesInColumn.txt", 'a+')
            self.logger.log(file, "Error Occured:: %s" % e)
            file.close()
            raise e
        file.close()