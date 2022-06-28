import pandas as pd
import os
import numpy as np
from application_logging.logger import App_Logger
from prediciton_data_validation.prediction_data_validation import PredicitonDataValidation
from data_preprocessing.preprocessing import PreProcessing
from file_operation.file_handler import FileHandler


class Prediciton:
    def __init__(self):
        self.logger = App_Logger()
        self.file_object = open("Prediction_Log/Prediction.txt", "a+")
        self.pred_data_val = PredicitonDataValidation()

    def predict(self):
        try:
            self.logger.log(self.file_object, 'Start of Prediction')
            self.preprocessing = PreProcessing(self.file_object, self.logger)
            self.model = FileHandler(self.file_object, self.logger)
            file = os.listdir('Prediction_Files/')[0]
            dataframe = pd.read_csv('Prediction_Files/' + file)
            self.csv = dataframe.copy()
            self.csv = self.preprocessing.encode_data(self.csv, "Region")
            self.csv = np.array(self.csv)
            random_forest_regressor = self.model.loadModel('RandomForestRegressor')
            predicted = random_forest_regressor.predict(self.csv)
            self.logger.log(self.file_object, "Prediction complete")
            return np.round(predicted, 2)
        except Exception as e:
            self.logger.log(self.file_object, "Error occured while prediction" + str(e))
            raise e
