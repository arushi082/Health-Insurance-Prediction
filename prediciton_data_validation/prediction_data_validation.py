from application_logging.logger import App_Logger
import json
import os
import shutil
import pandas as pd
import numpy as np

class PredicitonDataValidation:
    def __init__(self):
        self.logger = App_Logger()
        self.schema = 'prediction_schema.json'
    def deletePredictionFiles(self):
        file = open("Prediction_Log/fileHandling.txt","a+")
        try:
            self.logger.log(file,"Entered the delete prediciton file method of the prediction data validation class")
            shutil.rmtree('Prediction_Files/')
            self.logger.log(file,'Predciton_files deleted')
        except Exception as e:
            self.logger.log(file,'Error occured in deleting the prediction file'+str(e))
            self.logger.log(file,'Failed to delete folder')
            file.close()
        file.close()
    def createPredictionFiles(self, folderName):
        file = open("Prediction_Log/fileHandling.txt",'a+')
        try:
            self.logger.log(file,'Enter the create Prediction File method of Predcititon Data Validation')
            os.mkdir(f'{folderName}/')
            self.logger.log(file,'Prediciton_Files created')
        except Exception as e:
            self.logger.log(file,'Error occured im creating the folder in createPredictionFiles method of prediciton data validation ','Error')
            self.logger.log(file,'Failed to create folder')

    def getSchemaValues(self):

        file = open("Prediction_Log/fileHandling.txt", 'a+')
        try:
            self.logger.log(file,'Entered the setSchema Method of the predciton Data Validation class')
            with open(self.schema,'r') as f:
                dic = json.load(f)
                f.close()
            column_names = dic["columnNames"]
            region = dic["region"]
            required_columns = dic["RequiredColumns"]
            message = "region:"+str(region) +"\t"+"REquired Columns:"+str(required_columns)+"\n"
            self.logger.log(file,message)
        except Exception as e:
            file = open("Prediction_Log/valuesFromSchemaLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e
        return region,column_names,required_columns
    def validate_data_type(self):
        f = open("Prediction_Log/columnValidationLog.txt", 'a+')
        try:
            self.logger.log(f,"Validate Column Data Type")
            for file in os.listdir('Prediction_Files/'):
                csv = pd.read_csv('Prediction_Files/'+file)
                for i in csv.columns:
                    if csv[[i]].dtypes[0] == np.int64 or csv[[i]].dtypes[0] == np.float64:
                        pass
                    elif i =='Region' and csv[[i]].dtypes[0] == np.dtype('O'):
                        pass
                    else:
                        self.logger.log(f,"Failed Validation ")
                        raise Exception('Different dtypes found')
                self.logger.log(f,"Data Validation Complete")
        except Exception as e:
            self.logger.log(f,"Error occured in Validating dtypes"+str(e))
            self.logger.log(f,'Failed to validate dtypes')
            raise e