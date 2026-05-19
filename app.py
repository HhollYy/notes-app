from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    color = db.Column(db.String(20), default='#EFCE7B')
    created_at = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)

"""@app.route('/')
def home():
    notes = Note.query.all()
    for note in notes:
        print(f"Note: {note.title}, Color: {note.color}")
    return render_template("home.html", notes=notes)"""


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    color = request.form['color']
    new_note = Note(title=title, content=content, color=color)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("home"))

'''@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    color = request.form.get('color', 'NO COLOR FOUND')
    print(f"COLOR RECEIVED: {color}")
    new_note = Note(title=title, content=content, color=color)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("home"))'''


@app.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.color = request.form['color']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('note.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)
