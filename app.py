
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load("fever_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get values from the form
    temperature = float(request.form["temperature"])
    cough = int(request.form["cough"])
    headache = int(request.form["headache"])
    body_pain = int(request.form["body_pain"])

    # Model expects exactly 4 features
    input_data = [[
        temperature,
        cough,
        headache,
        body_pain
    ]]

    # Make prediction
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        result = "Fever Detected"
    else:
        result = "No Fever Detected"

    return render_template(
        "index.html",
        prediction=result
    )


if __name__ == "__main__":
    app.run(debug=True)
