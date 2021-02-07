from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Database where notes are stored

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note %r>' % self.id

# Add the note, and return to index

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        note_content = request.form['content']
        new_note = Todo(content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error while adding your note!"
    else:
        notes = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', notes=notes)


# Delete function

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error while deleting your note!"

# Update function

@app.route('/update/<int:id>', methods=['GET', 'POST']) # send to update page
def update(id):
    note = Todo.query.get_or_404(id)

    if request.method == 'POST':
        note.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')    # return to index page after updating
        
        except:
            return "An error occured while updating your note!"
            
    else:
        return render_template('update.html', note=note)

if __name__ == "__main__":
    app.run(debug=True)