from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    test_string = request.form.get("test_string")
    regex_pattern = request.form.get("regex_pattern")
    matched_strings = re.findall(regex_pattern, test_string)
    return render_template("results.html", matched_strings=matched_strings)

@app.route("/validate-email", methods=["POST"])
def validate_email():
    email = request.form.get("email")
    if re.match(r'^[\w\.-]+@[\w\.-]+$', email):
        is_valid = True
    else:
        is_valid = False
    return render_template("validate_email.html", email=email, is_valid=is_valid)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
