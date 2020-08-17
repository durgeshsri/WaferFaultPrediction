#from datetime import datetime
from os import listdir
import pandas
from logger import App_Logger


class DataTransformPredict:

     """
                  This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

                  Written By: iNeuron Intelligence
                  Version: 1.0
                  Revisions: None

                  """

     def __init__(self):
          self.GoodDataPath = "PredictionRawFilesValidated/GoodRaw"
          self.logger = App_Logger()


     def ReplaceMissingWithNull(self):

          """
                                  Method Name: ReplaceMissingWithNull
                                  Description: This method replaces the missing values in columns with "NULL" to
                                               store in the table. We are using substring in the first column to
                                               keep only "Integer" data for ease up the loading.
                                               This column is anyways going to be removed during prediction.

                                   Written By: Durgesh Kumar
                                  Version: 1.0
                                  Revisions: None

                                          """

          try:
               file = open("PredictionLog/DataTransformLog.txt", 'a+')
               onlyfiles = [f for f in listdir(self.GoodDataPath)]
               for files in onlyfiles:
                    csv = pandas.read_csv(self.GoodDataPath+"/" + files)
                    csv.fillna('NULL',inplace=True)
                    csv['Wafer'] = csv['Wafer'].str[6:]
                    csv.to_csv(self.GoodDataPath+ "/" + files, index=None, header=True)
                    self.logger.log(file," %s: File Transformed successfully!!" % files)

          except Exception as e:
              file = open("PredictionLog/DataTransformLog.txt", 'a+')
              self.logger.log(file, "Data Transformation failed because:: %s" % e)
              file.close()
              raise e
