from flask import Flask, render_template
app = Flask(__name__)

@app.route("/login")
def layout():
	return render_template('login.html')

@app.route("/report")
def report():
	return render_template('report.html')

@app.route("/add_record")
def add_record():
	return render_template('add_record.html')

if __name__ == "__main__":
    app.run(debug=True)