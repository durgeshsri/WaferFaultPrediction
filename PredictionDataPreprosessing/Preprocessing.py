import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class Preprocessor:
    """
            This class shall  be used to clean and transform the data before training.

            Written By: Durgesh Kumar
            Version: 1.0
            Revisions: None

            """

    def __init__(self,FileObject,Logger):
        self.file = FileObject
        self.logger = Logger


    def RemoveColumns(self,data,Columns):
        """
                        Method Name: RemoveColumns
                        Description: This method removes the given columns from a pandas dataframe.
                        Output: A pandas DataFrame after removing the specified columns.
                        On Failure: Raise Exception

                        Written By: Durgesh Kumar
                        Version: 1.0
                        Revisions: None

                """


        self.logger.log(self.file,"Started Removing columns using RemoveColumns method from Preprocessor Class")
        self.data = data
        self.columns = Columns

        try:
            # drop the labels specified in the columns
            self.UsefullData = self.data.drop(labels=self.columns,axis=1)
            self.logger.log(self.file,'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.UsefullData
        except Exception as e:
            self.logger.log(self.file,'Exception occured in remove_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()


    def SeperateLabelFeatures(self,data,LabelColumnName):

        """
                                Method Name: SeperateLabelFeatures
                                Description: This method separates the features and a Label Coulmns.
                                Output: Returns two separate Dataframes, one containing features and the other containing Labels .
                                On Failure: Raise Exception

                                Written By: Durgesh Kumar
                                Version: 1.0
                                Revisions: None

                        """

        self.logger.log(self.file, 'Entered the SeperateLabelFeatures method of the Preprocessor class')
        try:
            self.X = data.drop(labels=LabelColumnName,axis=1)  # drop the columns specified and separate the feature columns
            self.Y = data[LabelColumnName]  # Filter the Label columns
            self.logger.log(self.file,'Label Separation Successful. Exited the SeperateLabelFeatures method of the Preprocessor class')
            return self.X, self.Y
        except Exception as e:
            self.logger.log(self.file,'Exception occured in SeperateLabelFeatures method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Label Separation Unsuccessful. Exited the SeperateLabelFeatures method of the Preprocessor class')
            raise Exception()


    def IsNullPresent(self,data):
        """
                                Method Name: IsNullPresent
                                Description: This method checks whether there are null values present in the pandas Dataframe or not.
                                Output: Returns a Boolean Value. True if null values are present in the DataFrame, False if they are not present.
                                On Failure: Raise Exception

                                Written By: Durgesh Kumar
                                Version: 1.0
                                Revisions: None

                        """
        self.logger.log(self.file, 'Entered the IsNullPresent method of the Preprocessor class')
        self.NullPresent = False
        try:
            self.NullCounts=data.isna().sum() # check for the count of null values per column
            for i in self.NullCounts:
                if i>0:
                    self.NullPresent=True
                    break
            if(self.NullPresent): # write the logs to see which columns have null values
                DataframeWithNull = pd.DataFrame()
                DataframeWithNull['columns'] = data.columns
                DataframeWithNull['missing values count'] = np.asarray(data.isna().sum())
                DataframeWithNull.to_csv('TrainingPreprocessingData/NullValues.csv') # storing the null column information to file
            self.logger.log(self.file,'Finding missing values is a success.Data written to the null values file. Exited the IsNullPresent method of the Preprocessor class')
            return self.NullPresent
        except Exception as e:
            self.logger.log(self.file,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Finding missing values failed. Exited the IsNullPresent method of the Preprocessor class')
            raise Exception()


    def ImputeMissingValues(self, data):
        """
                                        Method Name: ImputeMissingValues
                                        Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
                                        Output: A Dataframe which has all the missing values imputed.
                                        On Failure: Raise Exception

                                        Written By: Durgesh Kumar
                                        Version: 1.0
                                        Revisions: None
                     """
        self.logger.log(self.file, 'Entered the ImputeMissingValues method of the Preprocessor class')
        self.data = data
        try:
            Imputer = KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.NewArray = Imputer.fit_transform(self.data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            self.NewData = pd.DataFrame(data=self.NewArray, columns=self.data.columns)
            self.logger.log(self.file, 'Imputing missing values Successful. Exited the ImputeMissingValues method of the Preprocessor class')
            return self.NewData
        except Exception as e:
            self.logger.log(self.file,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Imputing missing values failed. Exited the ImputeMissingValues method of the Preprocessor class')
            raise Exception()


    def GetColumnsWithZeroStdDeviation(self,data):
        """
                                                Method Name: GetColumnsWithZeroStdDeviation
                                                Description: This method finds out the columns which have a standard deviation of zero.
                                                Output: List of the columns with standard deviation of zero
                                                On Failure: Raise Exception

                                                Written By: Durgesh Kumar
                                                Version: 1.0
                                                Revisions: None
                             """
        self.logger.log(self.file, 'Entered the GetColumnsWithZeroStdDeviation method of the Preprocessor class')
        self.columns = data.columns
        self.Data = data.describe()
        self.ColumnsToDrop = []
        try:
            for x in self.columns:
                if (self.Data[x]['std'] == 0): # check if standard deviation is zero
                    self.ColumnsToDrop.append(x)  # prepare the list of columns with standard deviation zero
            self.logger.log(self.file, 'Column search for Standard Deviation of Zero Successful. Exited the GetColumnsWithZeroStdDeviation method of the Preprocessor class')
            return self.ColumnsToDrop

        except Exception as e:
            self.logger.log(self.file,'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger.log(self.file, 'Column search for Standard Deviation of Zero Failed. Exited the GetColumnsWithZeroStdDeviation method of the Preprocessor class')
            raise Exception()



