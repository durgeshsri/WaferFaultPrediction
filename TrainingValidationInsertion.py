from TrainingRawDataValidation.RawValidation import RawDataValidation
from TrainingDataBaseOperation.DbOperation import DbOperation
from TrainingDataTransform.DataTransformation import DataTransform
from logger import App_Logger

class TrainValidation:
    def __init__(self,path):
        self.RawData = RawDataValidation(path)
        self.DataTransform = DataTransform()
        self.DbOperation = DbOperation()
        self.file = open("TrainingLog/TrainingMainLog.txt", 'a+')
        self.logger = App_Logger()


    def TrainValidation(self):
        try:
            self.logger.log(self.file, "Start of Validation of files!!!!!" )

            # extracting values from training schema
            LenghtOfDateStampInFile, LenghtOfTimeStampInFile, ColumnNames ,NumberOfColumn = self.RawData.ValuesFromSchema()

            # getting the regex defined to validate filename
            regex = self.RawData.RegexCreator()

            # validating filename of training files
            self.RawData.ValidateFileName(regex, LenghtOfDateStampInFile, LenghtOfTimeStampInFile)

            # validating column length in the file
            self.RawData.ValidateColumnLenght(NumberOfColumn)

            # validating if any column has all values missing
            self.RawData.ValidateMissingValuesInWholeColumn()
            self.logger.log(self.file, "Raw Data Validation Completed!!!!!")

            self.logger.log(self.file,"Starting Data Transformation!!!")
            # replacing blanks in the csv file with "Null" values
            self.DataTransform.ReplaceMissingWithNull()

            self.logger.log(self.file,"Data Transformation Completed!!")

            self.logger.log(self.file,"Start Creating Training Database and Tables on the basis of given schema!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.DbOperation.CreateTableInDB('Training', ColumnNames)
            self.logger.log(self.file,"Table Creation Completed!!!!")
            # insert csv files in the table
            self.DbOperation.InsertGoodDataIntoTable('Training')
            self.logger.log(self.file,"Insertion in Table completed!!!")

            # Delete the good data folder after loading files in table
            self.logger.log(self.file,"Deleting Good Data Folder!!!")
            self.RawData.DeleteExistingGoodDataTrainingFolder()
            self.logger.log(self.file,"Good Data Folder Deleted!!!")

            # Move the bad files to archive folder
            self.logger.log(self.file,"Moving Bad Files to Archive and Deleting Bad Files Folder!!")
            self.RawData.MoveBadFilesToArchiveBad()
            self.logger.log(self.file,"Bad Files Moved to Archive and Deleted Bad Files!!!")

            self.logger.log(self.file,"Validation Operation completed!!!")

            self.logger.log(self.file,"Extracting csv file From table")
            #export data in table to csvfile
            self.DbOperation.SelectingDataFromTableIntoCsv('Training')
            self.logger.log(self.file,"Successfully Extracted Files from Table!!!")



        except Exception as e:
            raise e







