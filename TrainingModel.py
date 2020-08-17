"""
This is the Entry point for Training the Machine Learning Model.

Written By: Durgesh Kumar
Version: 1.0
Revisions: None

"""

from sklearn.model_selection import train_test_split
from TrainingDataIngestion import DataLoader
from TrainingDataPreprocessing import Preprocessing, Clustering
from TrainingBestModelFinder import HyperParameterTuner
from TrainingFileOperations import FileOperations
import logger

class TrainModel:

    def __init__(self):
        self.logger = logger.App_Logger()
        self.file = open("TrainingLog/ModelTrainingLog.txt", 'a+')


    def TrainingModel(self):

        self.logger.log(self.file,"Start of the Training")
        try:
            #Loading the data
            DataGetter = DataLoader.DataGetter(self.file,self.logger)
            Data = DataGetter.GetData()

            """Doing the Preprocessing"""

            preprocessor = Preprocessing.Preprocessor(self.file,self.logger)
            Data = preprocessor.RemoveColumns(Data,['Wafer'])

            #Create Seperate Features and Target
            X,Y = preprocessor.SeperateLabelFeatures(Data,LabelColumnName='Output')

            # check if missing values are present in the dataset
            isNullPresent = preprocessor.IsNullPresent(X)

            # if missing values are there, replace them appropriately.
            if (isNullPresent):
                X = preprocessor.ImputeMissingValues(X)  # missing value imputation

            # check further which columns do not contribute to predictions
            # if the standard deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output both for good and bad sensors
            # prepare the list of such columns to drop

            ColumnsToDrop = preprocessor.GetColumnsWithZeroStdDeviation(X)
            X = preprocessor.RemoveColumns(X,ColumnsToDrop)

            """Applying the Clustering Approach """

            kmeans = Clustering.KMeansClustering(self.file, self.logger)  # object initialization.
            NumberOfClusters = kmeans.ElbowPlot(X)  # using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X = kmeans.CreateClusters(X, NumberOfClusters)

            # create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels'] = Y

            # getting the unique clusters from our dataset
            ListOfClusters = X['Cluster'].unique()

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in ListOfClusters:
                ClusterData=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                ClusterFeatures=ClusterData.drop(['Labels','Cluster'],axis=1)
                ClusterLabel= ClusterData['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(ClusterFeatures, ClusterLabel, test_size=1 / 3, random_state=355)

                model_finder=HyperParameterTuner.ModelFinder(self.file,self.logger) # object initialization

                #getting the best model for each of the clusters
                best_model_name,best_model=model_finder.GetBestModel(x_train,y_train,x_test,y_test)

                #saving the best model to the directory.
                file_op = FileOperations.FileOperations(self.file,self.logger)
                file_op.SaveModel(best_model,best_model_name+str(i))

            # logging the successful Training
            self.logger.log(self.file, 'Successful End of Training')
            self.file.close()

        except Exception:
            # logging the unsuccessful Training
            self.logger.log(self.file, 'Unsuccessful End of Training')
            self.file.close()
            raise Exception
















