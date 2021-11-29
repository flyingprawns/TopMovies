from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)

# ------- Create database ------- #
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------- Add bootstrap -------- #
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# ------- Create movie table ------- #
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(5000))
    img_url = db.Column(db.String(100))

    def __rep__(self):
        return f'<Movie: {self.title}>'
db.create_all()


# -------- WTForms for adding/rating movies -------- #
class AddMovieForm(FlaskForm):
    title = StringField(label='Movie title:', validators=[DataRequired()])
    submit = SubmitField(label='Add movie to list')


class RateMovieForm(FlaskForm):
    rating = FloatField(label='Your rating from 0.0 to 10.0:', validators=[DataRequired()])
    review = StringField(label='Your review:', validators=[DataRequired()])
    submit = SubmitField(label='Leave review')


# ------- Website Pages ------- #
@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", all_movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    edit_form = RateMovieForm()
    if edit_form.validate_on_submit():
        movie.rating = edit_form.rating.data
        movie.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        title = add_form.title.data
        year = 1111
        rating = 3
        new_movie = Movie(title=title, year=year, rating=rating)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", form=add_form)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
