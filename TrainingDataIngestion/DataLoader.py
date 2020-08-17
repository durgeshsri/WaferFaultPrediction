import pandas as pd

class DataGetter:


    """
    This class shall  be used for obtaining the data from the source for training.

    Written By: Durgesh Kumar
    Version: 1.0
    Revisions: None

    """
    def __init__(self,FileObject,Logger):
        self.TrainingFile = "TrainingFilesFromDB/InputFile.csv"
        self.FileObject = FileObject
        self.logger = Logger


    def GetData(self):

        """
        Method Name: GetData
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

         Written By: Durgesh Kumar
        Version: 1.0
        Revisions: None

        """

        self.logger.log(self.FileObject,"Start getting data from local")
        try:
            self.data = pd.read_csv(self.TrainingFile)  # reading the data file
            self.logger.log(self.FileObject,'Data Load Successful.Exited the GetData method of the DataGetter class')
            return self.data
        except Exception as e:
            self.logger.log(self.FileObject,'Exception occured in get_data method of the DataGetter class. Exception message: ' + str(e))
            self.logger.log(self.FileObject,'Data Load Unsuccessful.Exited the GetData method of the DataGetter class')
            raise Exception()

