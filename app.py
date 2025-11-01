from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load saved Random Forest model
model = joblib.load("house_price_model.pkl")

# Affordability classification based on predicted price
def classify_affordability(price):
    if price < 150000:
        return "Affordable"
    elif price < 300000:
        return "Mid-range"
    else:
        return "Luxury"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect inputs from form
        features = [
            float(request.form['OverallQual']),
            float(request.form['GrLivArea']),
            float(request.form['FirstFlrSF']),
            float(request.form['TotalBsmtSF']),
            float(request.form['SecondFlrSF']),
            float(request.form['BsmtFinSF1']),
            float(request.form['FullBath']),
            float(request.form['LotArea']),
            float(request.form['GarageArea']),
            float(request.form['GarageCars'])
        ]

        # Prepare input for model
        final_features = np.array(features).reshape(1, -1)

        # Predict price
        prediction = model.predict(final_features)[0]
        prediction_rounded = round(prediction, 2)

        # Classify affordability
        affordability = classify_affordability(prediction_rounded)

        # Return result
        return render_template('index.html',
                               prediction_text=f" ${prediction_rounded}",
                               affordability_text=f" {affordability}")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
