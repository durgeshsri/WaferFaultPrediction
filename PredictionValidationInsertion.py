from PredictionDataBaseOperation.DBOperation import dBOperation
from PredictionDataTransform.DataTransform import DataTransformPredict
from PredictionRawDataValidation.RawValidation import PredictionDataValidation
import logger


class PredictionValidation:


    def __init__(self,path):
        self.raw_data = PredictionDataValidation(path)
        self.dataTransform = DataTransformPredict()
        self.dBOperation = dBOperation()
        self.file = open("PredictionLog/PredictionMainLogs.txt", 'a+')
        self.logger = logger.App_Logger()




    def PredictionValidation(self):

        try:

            self.logger.log(self.file,'Start of Validation on files for prediction!!')
            #extracting values from prediction schema
            LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,noofcolumns = self.raw_data.valuesFromSchema()
            #getting the regex defined to validate filename
            regex = self.raw_data.ManualRegexCreation()
            #validating filename of prediction files
            self.raw_data.ValidationFileNameRaw(regex,LengthOfDateStampInFile,LengthOfTimeStampInFile)
            #validating column length in the file
            self.raw_data.ValidateColumnLength(noofcolumns)
            #validating if any column has all values missing
            self.raw_data.ValidateMissingValuesInWholeColumn()
            self.logger.log(self.file,"Raw Data Validation Complete!!")

            self.logger.log(self.file,("Starting Data Transforamtion!!"))
            #replacing blanks in the csv file with "Null" values to insert in table
            self.dataTransform.ReplaceMissingWithNull()

            self.logger.log(self.file,"DataTransformation Completed!!!")

            self.logger.log(self.file,"Creating Prediction_Database and tables on the basis of given schema!!!")
            #create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.createTableDb('Prediction',column_names)
            self.logger.log(self.file,"Table creation Completed!!")
            self.logger.log(self.file,"Insertion of Data into Table started!!!!")
            #insert csv files in the table
            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.logger.log(self.file,"Insertion in Table completed!!!")
            self.logger.log(self.file,"Deleting Good Data Folder!!!")
            #Delete the good data folder after loading files in table
            self.raw_data.DeleteExistingGoodDataTrainingFolder()
            self.logger.log(self.file,"Good_Data folder deleted!!!")
            self.logger.log(self.file,"Moving bad files to Archive and deleting Bad_Data folder!!!")
            #Move the bad files to archive folder
            self.raw_data.MoveBadFilesToArchiveBad()
            self.logger.log(self.file,"Bad files moved to archive!! Bad folder Deleted!!")
            self.logger.log(self.file,"Validation Operation completed!!")
            self.logger.log(self.file,"Extracting csv file from table")
            #export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Prediction')


        except Exception as e:
            raise e




