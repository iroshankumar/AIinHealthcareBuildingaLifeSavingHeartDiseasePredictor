
from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)


# Load all models
models = {
    "Logistic Regression": joblib.load("log_reg_model.pkl"),
    "Random Forest": joblib.load("rf_model.pkl"),
    "SVM": joblib.load("svm_model.pkl"),
    "KNN": joblib.load("knn_model.pkl")
}


categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
numerical_features = ['age', 'trestbps', 'chol', 'thalch', 'oldpeak', 'ca']

all_features = numerical_features + categorical_features


# Landing page
@app.route('/home')
def home():
    return render_template('home.html')

# Prediction page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get model choice
            model_choice = request.form['model_choice']
            model = models[model_choice]

            # Collect inputs
            input_data = {}
            for feature in numerical_features:
                input_data[feature] = float(request.form[feature])
            for feature in categorical_features:
                input_data[feature] = request.form[feature]

            # Convert to DataFrame
            input_df = pd.DataFrame([input_data])

            # Make prediction
            pred = model.predict(input_df)[0]
            if hasattr(model, "predict_proba"):
                pred_prob = np.max(model.predict_proba(input_df))
            else:
                pred_prob = None

            # Map target to human-readable
            if pred == 0:
                result = "No Heart Disease"
            else:
                result = f"Heart Disease (Severity {pred})"

            return render_template('index.html', result=result, probability=f"{pred_prob*100:.2f}%" if pred_prob else "N/A", models=list(models.keys()))
        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html', result=None, probability=None, models=list(models.keys()))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
