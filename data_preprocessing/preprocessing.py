import pandas as pd
from file_operation.file_handler import FileHandler


class PreProcessing:
    def __init__(self, file_object, logger_object):
        self.csv = None
        self.file_object = file_object
        self.logger = logger_object

    def encode_data(self, csv, column):

        try:
            self.logger.log(self.file_object, 'Entered the encode_data method of preprocessing class')
            file_handler = FileHandler(self.file_object, self.logger)
            encoder = file_handler.loadModel('OneHotEncoder')
            encoded_data = pd.DataFrame(encoder.transform(csv[[column]]))
            csv.drop([column], axis=1, inplace=True)
            self.csv = pd.concat([csv, encoded_data], axis=1, join='inner')
            self.logger.log(self.file_object, 'Encoding Completed')
            return self.csv
        except Exception as e:
            self.logger.log(self.file_object, "An error occured during encoding")
            raise e
