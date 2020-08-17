import pandas as pd

class DataGetterPred:
    """
    This class shall  be used for obtaining the data from the source for prediction.

    Written By: Durgesh Kumar
    Version: 1.0
    Revisions: None

    """
    def __init__(self, file, logger):
        self.predictionFile='PredictionFileFromDB/InputFile.csv'
        self.file = file
        self.logger = logger

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

         Written By: Durgesh Kumar
        Version: 1.0
        Revisions: None

        """
        self.logger.log(self.file,'Entered the get_data method of the DataGetterPred class')
        try:
            self.data= pd.read_csv(self.predictionFile) # reading the data file
            self.logger.log(self.file,'Data Load Successful.Exited the get_data method of the DataGetterPred class')
            return self.data
        except Exception as e:
            self.logger.log(self.file,'Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            self.logger.log(self.file,'Data Load Unsuccessful.Exited the get_data method of the DataGetterPred class')
            raise Exception()