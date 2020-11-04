from googlesheets import *
from flask import *
from twilioclient import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "ACc77f218525c945278cca5dfc56b8c56f"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # string of 20 character
    password = db.Column(db.String(60),nullable=False)


    def __repr__(self):
        return f"User('{self.username} {self.id}')"


@app.route("/", methods=["POST", "GET"])
def base():
    if "user" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route("/home", methods=["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        prevUser = session.pop("user",None)
        print(f"User: {prevUser} has been logged out")
    if request.method == "POST":
        userStatus = "normal"
        username = request.form["Username"]
        password = request.form["Password"]



        check = searchLogin(username,password)
        if check == True:
            session["user"] = username
            flash(f"{username} logged in successfully")
            return redirect(url_for("addnum"))
        elif check == False:
            flash(f"Username {username} is not found ")
            return redirect(url_for("signup"))
        elif check == -1:
            flash(f"Password does not match")
            return redirect(url_for("login"))
        elif check == "admin":
            flash(f"Welcome back {username}")
            return redirect(url_for("admin"))

    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        comfirmPassword = request.form["Confirm Password"]
        if password != comfirmPassword:
            flash("Your Password and Confirm password do not match")
            return redirect(url_for("signup"))
        else:
            addLogin(username,password)
            session["user"] = username
            flash(f"User: {username} has been successfully signed up")
            return redirect(url_for("addnum"))
    return render_template("signup.html")


@app.route("/addnum", methods=["POST", "GET"])
def addnum():
    if "user" not in session:
        flash("You are not logged in.")
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            name = request.form["Name"]
            phonenumber = request.form["Phone Number"]
            if len(phonenumber) > 10:
                flash("Phone Number should be in format 123456789x")
                return redirect("addnum")
            elif len(phonenumber) < 10:
                flash("A Phone Number should be ten numbers long")
                return redirect("addnum")
            else:
                foundNumber = findNumber(name)
                foundName = findName(phonenumber)
                if foundNumber != -1 and foundName != -1:
                    flash("User already in our database")
                elif foundNumber != -1 and foundName == -1:
                    flash("That name is already connected to a phone number")
                elif foundNumber == -1 and foundName != -1:
                    flash("That number is already connected to a name")
                else:
                    addNumberToGSheets(name, phonenumber)
                    flash(f"Added {name} to the number {phonenumber}")
                    return redirect(url_for("sendtxt"))

        return render_template("addnum.html")

#Gets SMS from twilio client
@app.route("/sms", methods=["POST", "GET"])
def sms():
    number = request.form["From"]
    message_body = request.form["Body"]
    number = number[2:]
    personName = findName(number)
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M")
    if personName == -1:
        income_message = [number, message_body, dt_string]
    elif personName != -1:
        income_message = [personName, message_body, dt_string]
    print(income_message)
    addMessages(income_message)
    print(f"Added {income_message} to DB")
    return "added"


@app.route("/sendtxt", methods=["POST", "GET"])
def sendtxt():
    if "user" not in session:
        flash("You are not logged in.")
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            name = request.form["Name"]
            phonenumber = request.form["Phone Number"]
            message = request.form["Message"]
            check = checkalreadyin(name, phonenumber)
            if check == False:
                flash("User not found, Please add them to our Database")
                return redirect(url_for("addnum"))
            else:
                if check == "foundname":
                    numberToText = findNumber(name)
                    sentMessageLogs(name,message)
                    sendSMS(numberToText, message)
                    flash(f"Sent {name} the message: {message}")
                elif check == "foundnumber":
                    numberToText = phonenumber
                    sentMessageLogs(phonenumber,message)
                    sendSMS(numberToText, message)
                    flash(f"Sent {numberToText} the message: {message}")

        return render_template("sendtext.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    prevUser = session.pop("user",None)
    flash("You have been logged out")
    return redirect(url_for("home"))

if __name__ == '__main__':
    
    app.run(debug=True)
