
from flask import Flask, render_template, request,redirect,url_for,session
import joblib

app = Flask(__name__)

app.secret_key="feversense_secret_key"  # Set a secret key for session management

# Load the trained model
model = joblib.load("fever_model.pkl")

# ---------------- LOGIN PAGE ----------------
@app.route("/")
def login_page():
    return render_template("login.html")


# ---------------- LOGIN CHECK ----------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    # Login details
    if username == "admin" and password == "1234":

        # Store login status
        session["logged_in"] = True

        # Go to FeverSense main page
        return redirect(url_for("home"))

    else:
        return render_template(
            "login.html",
            error="Invalid username or password"
        )


# ---------------- FEVER PAGE ----------------
@app.route("/home")
def home():

    # Don't allow access without login
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))

    return render_template("index.html")


# ---------------- PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():

    # Check whether user is logged in
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))



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
    # ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login_page"))


if __name__ == "__main__":
    app.run(debug=True)
