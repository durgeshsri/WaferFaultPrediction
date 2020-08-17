from PredictionDataIngestion.DataLoader import DataGetterPred
from PredictionFileOperation.FileOperations import FileOperations
from PredictionDataPreprosessing.Preprocessing import Preprocessor
from PredictionRawDataValidation.RawValidation import PredictionDataValidation
import logger
import pandas as pd

class Prediction:

    def __init__(self,path):
        self.file = open("PredictionLog/PredictionMainLogs.txt", 'a+')
        self.logger = logger.App_Logger()
        self.pred_data_val = PredictionDataValidation(path)

    def PredictionFromModel(self):

        try:
            self.pred_data_val.DeletePredictionFile() #deletes the existing prediction file from last run!
            self.logger.log(self.file,'Start of Prediction')
            data_getter=DataGetterPred(self.file,self.logger)
            data=data_getter.get_data()

            preprocessor = Preprocessor(self.file,self.logger)
            isNullPresent = preprocessor.IsNullPresent(data)
            if(isNullPresent):
                data = preprocessor.ImputeMissingValues(data)

            columnsToDrop  = preprocessor.GetColumnsWithZeroStdDeviation(data)
            data = preprocessor.RemoveColumns(data,columnsToDrop)

            file_loader = FileOperations(self.file, self.logger)
            kmeans = file_loader.LoadModel('KMeans')

            clusters = kmeans.predict(data.drop(['Wafer'], axis=1))  # drops the first column for cluster prediction
            data['clusters'] = clusters
            clusters = data['clusters'].unique()

            for i in clusters:

                cluster_data = data[data['clusters'] == i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data = data.drop(labels=['Wafer'], axis=1)
                cluster_data = cluster_data.drop(['clusters'], axis=1)
                model_name = file_loader.FindCorrectModelFile(i)
                model = file_loader.LoadModel(model_name)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(wafer_names, result)), columns=['Wafer', 'Prediction'])
                path = "PredictionOutputFile/Predictions.csv"
                result.to_csv("PredictionOutputFile/Predictions.csv", header=True,mode='a+')  # appends result to prediction file
            self.logger.log(self.file, 'End of Prediction')
        except Exception as ex:
            self.logger.log(self.file, 'Error occured while running the prediction!! Error:: %s' % ex)
            raise ex

        return path





