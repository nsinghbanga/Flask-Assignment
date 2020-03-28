import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "studentdb.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Student_info(db.Model):
    # title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    student_id = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    dob = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    amount_due = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return ("<student_ID: {}>".format(self.student_id),"<first_name: {}>".format(self.first_name),
"<last_name: {}>".format(self.last_name),"<dob: {}>".format(self.dob),"<amount_due: {}>".format(self.amount_due))

@app.route("/", methods=["GET", "POST"])
def home():
    student_db = None
    if request.form:
        try:
            student_info = Student_info(student_id=request.form.get("student_id"), first_name=request.form.get("first_name"), last_name=request.form.get("last_name"), dob=request.form.get("dob"), amount_due=request.form.get("amount_due"))
            db.session.add(student_info)
            db.session.commit()
        except Exception as e:
            print("Failed to add Student")
            print(e)
    student_db = Student_info.query.all()
    return render_template("home.html", student_db=student_db)

@app.route("/update", methods=["POST"])
def update():
    try:
        newstudent = request.form.get("newstudent")
        oldstudent = request.form.get("oldstudent")
        student_info = Student_info.query.filter_by(student_id=oldstudent).first()
        student_info.student_id = newstudent
        db.session.commit()
    except Exception as e:
        print("Couldn't update student_info student_id")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    student_id = request.form.get("student_id")
    student_info = Student_info.query.filter_by(student_id=student_id).first()
    db.session.delete(student_info)
    db.session.commit()
    return redirect("/")
  
if __name__ == "__main__":
    app.run(debug=True)