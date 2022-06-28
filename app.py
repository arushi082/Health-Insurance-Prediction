import pandas as pd
from flask_cors import cross_origin
from flask import Flask, request, render_template, redirect, url_for
from prediciton_data_validation.prediction_data_validation import PredicitonDataValidation
from prediciton_data_validation.prediction_validation import PredicitonValidation
from model_prediction.Prediction import Prediciton
from application_logging.logger import App_Logger

app = Flask(__name__)
logger = App_Logger()


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    try:
        pred_data_val = PredicitonDataValidation()
        pred_data_val.deletePredictionFiles()
        pred_data_val.createPredictionFiles('Prediction_Files')
        column_info = pred_data_val.getSchemaValues()
        region = column_info[0]
        return render_template('index.html', csv={'region': region})
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route("/input", methods=['POST'])
@cross_origin()
def manual_input():
    try:
        if request.method == 'POST':
            input_data = []
            pred_data_val = PredicitonDataValidation()
            required_columns = pred_data_val.getSchemaValues()[2]
            columns = pred_data_val.getSchemaValues()[1]
            selected = request.form.to_dict(flat=False)
            for i, v in enumerate(selected.keys()):
                if v in columns.keys():
                    property_col = columns[v][selected[v][0]]
                    input_data.append(property_col)
                else:
                    input_data.append(selected[v][0])
            pd.DataFrame([input_data], columns=required_columns).to_csv('Prediction_Files/Prediction.csv')
        return redirect(url_for('predict'))
    except Exception as e:
        message = 'Error :: ' + str(e)
        return render_template('exception.html', exception=message)


@app.route('/predict', methods=['GET'])
def predict():
    try:

        pred_val = PredicitonValidation()
        pred_val.validation()
        pred = Prediciton()
        output = pred.predict()
        return render_template('result.html', result={"output": output})
    except Exception as e:
        message = 'Error ::' + str(e)
        return render_template('exception.html', exception=message)


if __name__ == "__main__":
    app.run(debug=True)
