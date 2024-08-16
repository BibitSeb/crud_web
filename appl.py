from flask import Flask,render_template,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"
app.config["SECRET_KEY"] = "hi"
db=SQLAlchemy(app)


class Stud(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    age=db.Column(db.Integer)


@app.route("/")
def base():
    return render_template("base.html")

@app.route("/add",methods=["POST","GET"])
def add():
    if request.method=="POST":
        try:
            current_id=int(request.form['id'])
            current_name=request.form['nam']
            current_age=int(request.form['age'])
            if current_id <= 0:
                flash("ID must be a positive integer.", "warning")
                return redirect("/add")
            if current_age < 0:
                flash("Age must be a non-negative integer.", "warning")
                return redirect("/add")
            new_student = Stud(id=current_id, name=current_name, age=current_age)
            db.session.add(new_student)
            db.session.commit()
            flash("Student details is entered succesfully !","info")
            return redirect("/add")
        except ValueError:
            flash("Please enter a valid numeric value for ID and age.", "warning")  
            return redirect("/add")
        except Exception:
           # flash(f"{e}","info")
           #return redirect("/add")
            flash("UNIQUE constraint error occurred. Please try again later.", "error")
            return redirect("/add")
    else:
        return render_template("add.html")



@app.route("/update",methods=["POST","GET"])
def update():
    if request.method == "POST":
        try:
            id = int(request.form["id"])
            if id <= 0:
                flash("ID must be a positive integer.", "warning")
                return redirect("/update")
            new_name = request.form["nam"]
            new_age = int(request.form["age"])
            if new_age < 0:
                flash("Age must be a non-negative integer.", "warning")
                return redirect("/update")
            #student = Stud.query.get(id)
            student = Stud.query.filter_by(id=id).first()
            if student:
                student.name = new_name
                student.age = new_age
                db.session.commit()
                flash(f"Student with ID {id} has been updated.", "info")
                return redirect("/update")
            else:
                flash(f"No student found with ID {id}.", "error")
                return redirect("/update")
        except ValueError:
            flash("Please enter a valid numeric value for ID and age.", "warning")     
            return redirect("/update")
        except Exception as e:
            #print(f"ERROR:{e}")
            #return f"ERROR:{e}" 
            return redirect("/update")   
    else:
        return render_template("update.html")



@app.route("/delete",methods=["POST","GET"])
def delete():
    if request.method=="POST":
        try:
            id = int(request.form["id"])
            if id <= 0:
                flash("ID must be a positive integer.", "warning")
                return redirect("/delete")
            
            student = Stud.query.filter_by(id=id).first()
            if student:
                db.session.delete(student)
                db.session.commit()
                flash(f"Student with ID {id} has been deleted.", "info")
                return redirect("/delete")
            else:
                flash(f"No student found with ID {id}.", "error")
                return redirect("/delete")
        except ValueError:
            flash("Please enter a valid numeric value for ID.", "warning")      
            return redirect("/delete")  
        except Exception as e:
            return redirect("/delete")          
    else:
        return render_template("delete.html")


@app.route("/view")
def view():
    return render_template("view.html",values=Stud.query.all())

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)