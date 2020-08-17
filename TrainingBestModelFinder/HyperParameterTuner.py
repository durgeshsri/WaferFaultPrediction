from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score

class ModelFinder:
    """
                    This class shall  be used to find the model with best accuracy and AUC score.
                    Written By: Durgesh Kumar
                    Version: 1.0
                    Revisions: None

                    """

    def __init__(self, file, logger):
        self.file = file
        self.logger = logger
        self.rfc = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')



    def GetBestParamsForRandomForest(self,train_x,train_y):
        """
                                Method Name: GetBestParamsForRandomForest
                                Description: get the parameters for Random Forest Algorithm which give the best accuracy.
                                             Use Hyper Parameter Tuning.
                                Output: The model with the best parameters
                                On Failure: Raise Exception

                                Written By: Durgesh Kumar
                                Version: 1.0
                                Revisions: None

                        """
        self.logger.log(self.file, 'Entered the GetBestParamsForRandomForest method of the ModelFinder class')
        try:
            # initializing with different combination of parameters
            self.param_grid = {"n_estimators": [10, 50, 100, 130], "criterion": ['gini', 'entropy'],
                               "max_depth": range(2, 4, 1), "max_features": ['auto', 'log2']}

            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.rfc, param_grid=self.param_grid, cv=5,  verbose=3)
            #finding the best parameters
            self.grid.fit(train_x, train_y)

            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            #creating a new model with the best parameters
            self.rfc = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            # training the mew model
            self.rfc.fit(train_x, train_y)
            self.logger.log(self.file,'Random Forest best params: '+str(self.grid.best_params_)+'. Exited the GetBestParamsForRandomForest method of the ModelFinder class')

            return self.rfc
        except Exception as e:
            self.logger.log(self.file,'Exception occured in GetBestParamsForRandomForest method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Random Forest Parameter tuning  failed. Exited the GetBestParamsForRandomForest method of the ModelFinder class')
            raise Exception()


    def GetBestParamsForXgboost(self,train_x,train_y):

        """
                                        Method Name: GetBestParamsForXgboost
                                        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                                                     Use Hyper Parameter Tuning.
                                        Output: The model with the best parameters
                                        On Failure: Raise Exception

                                        Written By: Durgesh Kumar
                                        Version: 1.0
                                        Revisions: None

                                """
        self.logger.log(self.file,'Entered the GetBestParamsForXgboost method of the ModelFinder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_xgboost = {

                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]

            }
            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(XGBClassifier(objective='binary:logistic'),self.param_grid_xgboost, verbose=3,cv=5)
            # finding the best parameters
            self.grid.fit(train_x, train_y)

            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=1, max_depth=5, n_estimators=50)
            # training the mew model
            self.xgb.fit(train_x, train_y)
            self.logger.log(self.file,'XGBoost best params: ' + str(self.grid.best_params_) + '. Exited the GetBestParamsForXgboost method of the ModelFinder class')
            return self.xgb
        except Exception as e:
            self.logger.log(self.file,'Exception occured in GetBestParamsForXgboost method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger.log(self.file,'XGBoost Parameter tuning  failed. Exited the GetBestParamsForXgboost method of the ModelFinder class')
            raise Exception()




    def GetBestModel(self,train_x,train_y,test_x,test_y):
        """
                                                Method Name: GetBestModel
                                                Description: Find out the Model which has the best AUC score.
                                                Output: The best model name and the model object
                                                On Failure: Raise Exception

                                                Written By: Durgesh Kumar
                                                Version: 1.0
                                                Revisions: None

                                        """
        self.logger.log(self.file,'Entered the GetBestModel method of the ModelFinder class')
        # create best model for XGBoost
        try:
            self.xgboost= self.GetBestParamsForXgboost(train_x,train_y)
            self.PredictionXgboost = self.xgboost.predict(test_x) # Predictions using the XGBoost Model

            if len(test_y.unique()) == 1: #if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.XgboostScore = accuracy_score(test_y, self.PredictionXgboost)
                self.logger.log(self.file, 'Accuracy for XGBoost:' + str(self.XgboostScore))  # Log AUC
            else:
                self.XgboostScore = roc_auc_score(test_y, self.PredictionXgboost) # AUC for XGBoost
                self.logger.log(self.file, 'AUC for XGBoost:' + str(self.XgboostScore)) # Log AUC

            # create best model for Random Forest
            self.random_forest=self.GetBestParamsForRandomForest(train_x,train_y)
            self.PredictionRandomForest=self.random_forest.predict(test_x) # prediction using the Random Forest Algorithm

            if len(test_y.unique()) == 1:#if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y,self.PredictionRandomForest)
                self.logger.log(self.file, 'Accuracy for RF:' + str(self.random_forest_score))
            else:
                self.random_forest_score = roc_auc_score(test_y, self.PredictionRandomForest) # AUC for Random Forest
                self.logger.log(self.file, 'AUC for RF:' + str(self.random_forest_score))

            #comparing the two models
            if(self.random_forest_score <  self.XgboostScore):
                return 'XGBoost',self.xgboost
            else:
                return 'RandomForest',self.random_forest

        except Exception as e:
            self.logger.log(self.file,'Exception occured in GetBestModel method of the ModelFinder class. Exception message:  ' + str(e))
            self.logger.log(self.file,'Model Selection Failed. Exited the GetBestModel method of the ModelFinder class')
            raise Exception()
