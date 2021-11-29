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
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(5000))
    img_url = db.Column(db.String(100))

    def __rep__(self):
        return f'<Movie: {self.title}>'
db.create_all()


# -------- Form for rating a movie -------- #
class RateMovieForm(FlaskForm):
    rating = FloatField(label='Your rating from 0.0 to 10.0:', validators=[DataRequired()])
    review = StringField(label='Your review:', validators=[DataRequired()])
    submit = SubmitField(label='Leave review')


# # ----- TESTING: add a movie ----- #
# new_movie = Movie(
#     title="Phone Booth 2",
#     year=2003,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth (AGAIN), pinned down by an "
#                 "extortionist's sniper rifle (AGAIN). Unable to leave or receive outside help, Stuart's "
#                 "negotiation with the caller leads (AGAIN) to a jaw-dropping climax.",
#     rating=7.1,
#     ranking=19,
#     review="My favourite character was the caller (AGAIN).",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


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


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
