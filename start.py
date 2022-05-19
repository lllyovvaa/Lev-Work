# from collections import namedtuple
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
# import psycopg2

# connection = psycopg2.connect(user="Lev", password="1234")


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///template.db"
db = SQLAlchemy(app)


class Firstname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name, secondname, about):
        self.name = name.strip()
        self.secondname = secondname
        self.about = about


class Secondname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)

    firstname_id = db.Column(db.Integer, db.ForeignKey('firstname.id'), nullable=False)
    firstname = db.relationship('Firstname', backref=db.backref('names'))


db.drop_all()


db.create_all()


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', names=Firstname.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    name = request.form['name']
    secondname = request.form['secondname']
    about = request.form['about']

    db.session.add(Firstname(name, secondname, about))
    db.session.commit()

    return redirect(url_for('main'))
