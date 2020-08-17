from os import listdir
import pandas as pd
from logger import App_Logger

class DataTransform:
    """
                   This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

                   Written By: Durgesh Kumar
                   Version: 1.0
                   Revisions: None

    """

    def __init__(self):
        self.GoodDataPath = "TrainingRawValidatedFiles/GoodRaw"
        self.logger = App_Logger()


    def ReplaceMissingWithNull(self):
        """
                                                   Method Name: ReplaceMissingWithNull
                                                   Description: This method replaces the missing values in columns with "NULL" to
                                                                store in the table. We are using substring in the first column to
                                                                keep only "Integer" data for ease up the loading.
                                                                This column is anyways going to be removed during training.

                                                    Written By: Durgesh Kumar
                                                   Version: 1.0
                                                   Revisions: None

        """

        file = open("TrainingLog/DataTransformLog.txt",'a+')
        try:
            OnlyFiles = [f for f in listdir(self.GoodDataPath)]
            for files in OnlyFiles:
                csv = pd.read_csv(self.GoodDataPath+"/"+files)
                csv.fillna('NULL', inplace=True)
                csv['Wafer'] = csv['Wafer'].str[6:]
                csv.to_csv(self.GoodDataPath + "/" + files, index = None, header=True)
                self.logger.log(file, "%s File Transformed Successfully!!!!")

        except Exception as e:
            self.logger.log(file, "Data Transformed failed!!  : %s" %e)
            file.close()
        file.close()





