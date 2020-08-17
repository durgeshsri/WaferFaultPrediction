import os
import re
import json
import shutil
import pandas as pd
from logger import App_Logger
from os import listdir
from datetime import datetime


class RawDataValidation:
    """
                 This class shall be used for handling all the validation done on the Raw Training Data!!.

                 Written By: Durgesh Kumar
                 Version: 1.0
                 Revisions: None

             """
    def __init__(self,path):
        self.batch_files = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

    def ValuesFromSchema(self):
        """
                                Method Name: ValuesFromSchema
                                Description: This method extracts all the relevant information from the pre-defined "Schema" file.
                                Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
                                On Failure: Raise ValueError,KeyError,Exception

                                 Written By: Durgesh Kumar
                                Version: 1.0
                                Revisions: None

                                        """
        try:
            with open(self.schema_path, 'r') as f:
                dict = json.load(f)
                f.close()
            FileName = dict['SampleFileName']
            LengthOfDateStamp = dict["LengthOfDateStampInFile"]
            LenghtOfTimeStamp = dict["LengthOfTimeStampInFile"]
            ColumnNames = dict["ColName"]
            NumberOfColumns = dict["NumberofColumns"]

            file = open("TrainingLog/ValuesFromSchemaValidation.txt", 'a+')
            message = "LengthOfDateStampInFile:: %s" % LengthOfDateStamp + "\t" + "LengthOfTimeStampInFile:: %s" % LenghtOfTimeStamp + "\t " + "NumberofColumns:: %s" % NumberOfColumns + "\n"
            self.logger.log(file, message)
            file.close()

        except ValueError:
            file = open("TrainingLog/ValuesFromSchemaValidation.txt", 'a+')
            self.logger.log(file,"ValueError: Value not found inside schema_training.json")
            file.close()
            raise ValueError
        except KeyError:
            file = open("TrainingLog/ValuesFromSchemaValidation.txt", 'a+')
            self.logger.log(file,"KeyError:Key Value error incorrect key passed")
            file.close()
            raise KeyError
        except Exception as e:
            file = open("TrainingLog/ValuesFromSchemaValidation.txt", 'a+')
            self.logger.log(file,str(e))
            file.close()
            raise e
        return LengthOfDateStamp,LenghtOfTimeStamp,ColumnNames,NumberOfColumns


    def RegexCreator(self):

        """
                                        Method Name: RegexCreator
                                        Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                                                    This Regex is used to validate the filename of the training data.
                                        Output: Regex pattern
                                        On Failure: None

                                         Written By: Durgesh Kumar
                                        Version: 1.0
                                        Revisions: None

                                                """
        regex = "['wafer']+['\_'']+[\d_]+[\d_]+\.csv"
        return regex


    def CreateDirectoryForGoodBadRawData(self):
        """
                                              Method Name: CreateDirectoryForGoodBadRawData
                                              Description: This method creates directories to store the Good Data and Bad Data
                                                            after validating the training data.

                                              Output: None
                                              On Failure: OSError

                                               Written By: Durgesh Kumar
                                              Version: 1.0
                                              Revisions: None

                                                      """

        try:
            path = os.path.join("TrainingRawValidatedFiles/"+"GoodRaw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("TrainingRawValidatedFiles/" + "BadRaw/")
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as ex:
            file = open("TrainingLog/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while creating Directory %s:" %ex)
            file.close()
            raise OSError

    def DeleteExistingGoodDataTrainingFolder(self):
        """
                                                    Method Name: DeleteExistingGoodDataTrainingFolder
                                                    Description: This method deletes the directory made  to store the Good Data
                                                                  after loading the data in the table. Once the good files are
                                                                  loaded in the DB,deleting the directory ensures space optimization.
                                                    Output: None
                                                    On Failure: OSError

                                                     Written By: Durgesh Kumar
                                                    Version: 1.0

                                         Revisions: None

                                                            """

        try:
            path = 'TrainingRawValidatedFiles/'
            if os.path.isdir(path+'GoodRaw/'):
                shutil.rmtree(path + 'GoodRaw/')
                file = open("TrainingLog/GeneralLog.txt", 'a+')
                self.logger.log(file,"GoodRaw Directory deleted Successfully!!!")
                file.close()
        except OSError as ex:
            file = open("TrainingLog/GeneralLog.txt", 'a+')
            self.logger.log(file, "Error while Deleting Directory!!! : %s" %ex)
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
            path = 'TrainingRawValidatedFiles/'
            if os.path.isdir(path+'BadRaw/'):
                shutil.rmtree(path + 'BadRaw/')
                file = open('TrainingLog/GeneralLog.txt', 'a+')
                self.logger.log(file,"BadRaw Directory Deleted before starting Validation!!")
                file.close()
        except OSError as s:
            file = open('TrainingLog/GeneralLog.txt', 'a+')
            self.logger.log(file, "Error while deleting directory : %s" %s)
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
        date =  now.date()
        time = now.strftime("%H%M%S")
        try:

            source = 'TrainingRawValidatedFiles/BadRaw/'
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                destination = 'TrainingArchiveBadData/BadData_' + str(date)+"_"+str(time)
                if not os.path.isdir(destination):
                    os.makedirs(destination)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(destination):
                        shutil.move(source+f,destination)

                file = open('TrainingLog/GeneralLog.txt', 'a+')
                self.logger.log(file,'Bad files moved to archive')
                path = 'TrainingRawValidatedFiles/'
                if os.path.isdir(path + 'BadRaw/'):
                    shutil.rmtree(path + 'BadRaw/')
                    self.logger.log(file, "Bad Raw Data Folder Deleted successfully!!")
                    file.close()

        except Exception as e:
            file = open("TrainingLog/GeneralLog.txt", 'a+')
            self.logger.log(file,"Error while moving bad data to archive : %s" %e)
            file.close()
            raise e



    def ValidateFileName(self,regex,LengthOfDateStamp,LenghtOfTimeStamp):
        """
                            Method Name: ValidateFileName
                            Description: This function validates the name of the training csv files as per given name in the schema!
                                         Regex pattern is used to do the validation.If name format do not match the file is moved
                                         to Bad Raw Data folder else in Good raw data.
                            Output: None
                            On Failure: Exception

                             Written By: Durgesh Kumar
                            Version: 1.0
                            Revisions: None

                        """
        # delete directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.DeleteExistingGoodDataTrainingFolder()
        self.DeleteExistingBadDataTrainingFolder()

        # create new directories
        self.CreateDirectoryForGoodBadRawData()
        onlyfiles = [f for f in listdir(self.batch_files)]
        # Batch_Directory is where user puts all data.
        try:
            file = open("TrainingLog/NameValidationLog.txt", 'a+')
            self.logger.log(file,"File Name Validation Started")
            for filename in onlyfiles:
                if (re.match(regex, filename)):
                    split_at_dot = re.split('.csv',filename)
                    split_at_dot = re.split('_',split_at_dot[0])
                    if len(split_at_dot[1]) == LengthOfDateStamp:
                        if len(split_at_dot[2]) == LenghtOfTimeStamp:
                            shutil.copy('TrainingBatchFiles/'+filename,"TrainingRawValidatedFiles/GoodRaw")
                            self.logger.log(file,"Valid File name!!! File moved to GoodRaw: %s" %filename)
                        else:
                            shutil.copy("TrainingBatchFiles/"+filename,"TrainingRawValidatedFiles/BadRaw")
                            self.logger.log(file,"Invalid File Name!!! File moved to Bad Raw Folder:%s" %filename)
                    else:
                        shutil.copy("TrainingBatchFiles/" + filename, "TrainingRawValidatedFiles/BadRaw")
                        self.logger.log(file, "Invalid File Name!!! File moved to Bad Raw Folder:%s" %filename)

                else:
                    shutil.copy("TrainingBatchFiles/" + filename, "TrainingRawValidatedFiles/BadRaw")
                    self.logger.log(file, "Invalid File Name!!! File moved to Bad Raw Folder:%s" %filename)
            self.logger.log(file,"File Name Validation Completed")
            file.close()

        except Exception as e:
            file = open("TrainingLog/NameValidationLod.txt",'a+')
            self.logger.log(file, "Error Occured While Validating FileName :%s" %e)
            file.close()
            raise e



    def ValidateColumnLenght(self,NumberOfColumns):
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
            file = open("TrainingLog/ColumnValidation.txt",'a+')
            self.logger.log(file,"Columns Lenght Validation Start")
            for files in listdir('TrainingRawValidatedFiles/GoodRaw/'):
                csv = pd.read_csv("TrainingRawValidatedFiles/GoodRaw/"+files)
                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move("TrainingRawValidatedFiles/GoodRaw/"+files,"TrainingRawValidatedFiles/BadRaw")
                    self.logger.log(file,"Invalid Column Lenght for the file!! file moved to Bad Raw Folder: %s" %files)
            self.logger.log(file,"Column Lenght validation Completed!!")
            file.close()

        except OSError:
            file = open("TrainingLog/ColumnValidation.txt",'a+')
            self.logger.log(file,"Error Occured while Moving the file: %s" %OSError)
            file.close()
            raise OSError
        except Exception as e:
            file = open("TrainingLog/ColumnValidation.txt",'a+')
            self.logger.log(file,"Error Occured: %s" %e)
            file.close()
            raise e


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
            file = open("TrainingLog/MissingValuesInColumn.txt", 'a+')
            self.logger.log(file,'Missing Value Validation Started!!')
            for files in listdir('TrainingRawValidatedFiles/GoodRaw/'):
                csv = pd.read_csv("TrainingRawValidatedFiles/GoodRaw/"+files)
                count = 0
                for columns in csv:
                    if (len(csv[columns])-csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("TrainingRawValidatedFiles/GoodRaw/"+files,"TrainingRawValidatedFiles/BadRaw/")
                        self.logger.log(file,"Invalid Column Lenght for the file!! File Moved To Bad Raw Folder: %s" %files)
                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0":"Wafer"}, inplace = True)
                    csv.to_csv("TrainingRawValidatedFiles/GoodRaw/"+files , index=None, header=True)
            self.logger.log(file,"Missing Value Validation completed!!")
            file.close()
        except OSError:
            file = open("TrainingLog/MissingValuesInColumn.txt", 'a+')
            self.logger.log(file,"Error Occured While Moving the files: %s" %OSError)
            file.close()
            raise OSError
        except Exception as e:
            file = open("TrainingLog/MissingValuesInColumn.txt", 'a+')
            self.logger.log(file,"Error Occured: %s" %e)
            file.close()
            raise e













