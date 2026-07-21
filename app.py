import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# -------------------- HOME --------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------- REGISTER --------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        village = request.form["village"]
        password = generate_password_hash(request.form["password"])

        # Check if email already exists
        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already registered!")
            return redirect(url_for("register"))

        # Save user
        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            village=village,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful! Please Login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------- LOGIN --------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.fullname
            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")


# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user=session["user"]
    )


# -------------------- WEATHER --------------------
@app.route("/weather", methods=["GET", "POST"])
def weather():

    if "user" not in session:
        return redirect(url_for("login"))

    weather = None
    error = None

    if request.method == "POST":

        city = request.form["city"]

        api_key = "92db5f74d550a7e2a7150ffb4f6992eb"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        print(data)   # For debugging

        if str(data.get("cod")) == "200":

            weather = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"]
            }

        else:
            error = data.get("message", "City not found.")

    return render_template(
        "weather.html",
        weather=weather,
        error=error
    )
# -------------------- CROPS --------------------
@app.route("/crops", methods=["GET", "POST"])
def crops():

    if "user" not in session:
        return redirect(url_for("login"))

    recommendation = None

    if request.method == "POST":

        soil = request.form["soil"]
        season = request.form["season"]

        crop_data = {

            ("Black", "Kharif"): "Cotton, Soybean, Tur",
            ("Black", "Rabi"): "Wheat, Gram",

            ("Red", "Kharif"): "Groundnut, Millets",
            ("Red", "Rabi"): "Pulses",

            ("Alluvial", "Kharif"): "Rice, Sugarcane",
            ("Alluvial", "Rabi"): "Wheat, Mustard",

            ("Sandy", "Summer"): "Watermelon, Groundnut",

            ("Clay", "Kharif"): "Rice",

            ("Loamy", "Rabi"): "Potato, Wheat, Onion"
        }

        recommendation = crop_data.get(
            (soil, season),
            "No crop recommendation available."
        )

    return render_template(
        "crops.html",
        recommendation=recommendation
    )

# -------------------- FARM DIARY --------------------
@app.route("/diary")
def diary():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("diary.html")


# -------------------- GOVERNMENT SCHEMES --------------------
@app.route("/schemes")
def schemes():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("schemes.html")


# -------------------- FARMING TIPS --------------------
@app.route("/tips")
def tips():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("tips.html")


# -------------------- FERTILIZER CALCULATOR --------------------
@app.route("/fertilizer")
def fertilizer():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("fertilizer.html")


# -------------------- LOGOUT --------------------
@app.route("/logout")
def logout():

    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True)