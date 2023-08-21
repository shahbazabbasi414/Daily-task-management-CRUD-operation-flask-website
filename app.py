from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if len(description) > 200:
        return "Description exceeds the maximum limit of 100 characters."
    
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if len(description) > 200:
            return "Description exceeds the maximum limit of 200 characters."
        
        task.title = title
        task.description = description
        db.session.commit()
        return redirect('/')
    
    return render_template('edit.html', task=task)


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

with app.app_context():
    db.create_all()

# ...

if __name__ == '__main__':
    app.run(debug=True)




