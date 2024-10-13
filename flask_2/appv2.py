from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable = False)
    created = db.Column(db.DateTime, default = datetime.now())
    
    def __repr__(self) -> str:
        return f"{self.task_id} - {self.title}"

@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        todo_title= request.form['title']
        todo_desc= request.form['desc']
        data = Todo(title=todo_title, description=todo_desc)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update(task_id):
    if request.method=='POST':
        todo_title= request.form['title']
        todo_desc= request.form['desc']
        data = Todo.query.filter_by(task_id=task_id).first()
        data.title= todo_title
        data.description= todo_desc
        db.session.add(data)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(task_id=task_id).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    todo = Todo.query.filter_by(task_id=task_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5500, debug =True)