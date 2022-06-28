from application_logging.logger import App_Logger
from prediciton_data_validation.prediction_data_validation import PredicitonDataValidation


class PredicitonValidation:
    def __init__(self):
        self.raw_data = PredicitonDataValidation()
        self.logger = App_Logger()

    def validation(self):
        f = open("Prediction_Log/Prediction_Log.txt", 'a+')
        try:

            self.logger.log(f, "Validation started for prediciton data")
            self.raw_data.validate_data_type()
            self.logger.log(f, "Datatype Validation Complete")
        except Exception as e:
            self.logger.log(f, "Error occured while performing validation")
            f.close()
            raise e
        f.close()
