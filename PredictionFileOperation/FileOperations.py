import pickle
import os
import shutil


class FileOperations:
    """
                    This class shall be used to save the model after training
                    and load the saved model for prediction.

                    Written By: Durgesh Kumar
                    Version: 1.0
                    Revisions: None

                    """
    def __init__(self,FileObject,Logger):
        self.file = FileObject
        self.logger = Logger
        self.ModelDirectory = "TrainingModels/"


    def SaveModel(self,Model,FileName):
        """
                    Method Name: SaveModel
                    Description: Save the model file to directory
                    Outcome: File gets saved
                    On Failure: Raise Exception

                    Written By: iNeuron Intelligence
                    Version: 1.0
                    Revisions: None
        """
        self.logger.log(self.file, 'Entered the SaveModel method of the FileOperations class')
        try:
            path = os.path.join(self.ModelDirectory, FileName)  # create seperate directory for each cluster
            if os.path.isdir(path):  # remove previously existing models for each clusters
                shutil.rmtree(self.ModelDirectory)
                os.makedirs(path)
            else:
                os.makedirs(path)  #
            with open(path + '/' + FileName + '.sav','wb') as f:
                pickle.dump(Model, f)  # save the model to file
            self.logger.log(self.file,'Model File ' + FileName + ' saved. Exited the SaveModel method of the FileOperations class')
            return 'success'
        except Exception as e:
            self.logger.log(self.file,'Exception occured in SaveModel method of the FileOperations class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Model File ' + FileName + ' could not be saved. Exited the SaveModel method of the FileOperations class')
            raise Exception()


    def LoadModel(self,filename):
        """
                    Method Name: LoadModel
                    Description: load the model file to memory
                    Output: The Model file loaded in memory
                    On Failure: Raise Exception

                    Written By: Durgesh Kumar
                    Version: 1.0
                    Revisions: None
        """
        self.logger.log(self.file, 'Entered the LoadModel method of the FileOperations class')
        try:
            with open(self.ModelDirectory + filename + '/' + filename + '.sav','rb') as f:
                self.logger.log(self.file,'Model File ' + filename + ' loaded. Exited the LoadModel method of the FileOperations class')
                return pickle.load(f)
        except Exception as e:
            self.logger.log(self.file,'Exception occured in LoadModel method of the FileOperations class. Exception message:' + str(e))
            self.logger.log(self.file,'Model File ' + filename + ' could not be saved. Exited the LoadModel method of the FileOperations class')
            raise Exception()



    def FindCorrectModelFile(self,ClusterNumber):
        """
                            Method Name: FindCorrectModelFile
                            Description: Select the correct model based on cluster number
                            Output: The Model file
                            On Failure: Raise Exception

                            Written By: Durgesh Kumar
                            Version: 1.0
                            Revisions: None
                """
        self.logger.log(self.file, 'Entered the FindCorrectModelFile method of the File_Operation class')
        try:
            self.cluster_number= ClusterNumber
            self.FolderName=self.ModelDirectory
            self.list_of_model_files = []
            self.list_of_files = os.listdir(self.FolderName)
            for self.f in self.list_of_files:
                try:
                    if (self.f.index(str( self.cluster_number))!=-1):
                        self.model_name=self.f
                except:
                    continue
            self.model_name=self.model_name.split('.')[0]
            self.logger.log(self.file,'Exited the FindCorrectModelFile method of the ModelFinder class.')
            return self.model_name
        except Exception as e:
            self.logger.log(self.file,'Exception occured in FindCorrectModelFile of the ModelFinder class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Exited the FindCorrectModelFile of the ModelFinder class with Failure')
            raise Exception()



