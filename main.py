from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import os

app = Flask(__name__)

bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    cafe = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Location on Google Map (URL)", validators=[URL(message="Invalid URL")])
    img_url = StringField("Image URL", validators=[URL(message="Invalid URL")])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = SelectField("Has sockets", choices=[1, 0])
    has_toilet = SelectField("Has toilet", choices=[1, 0])
    has_wifi = SelectField("Has wifi", choices=[1, 0])
    can_take_calls = SelectField("Can take calls", choices=[1, 0])
    seats = SelectField("How many seats", choices=["10-20", "20-30", "30-40", "40-50", "50+"])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'style': 'margin-top: 10px'})


@app.route("/")
def home():
    cafes = Cafe.query.order_by(Cafe.id).all()
    return render_template("index.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form.get("cafe"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=int(request.form.get("has_toilet")),
            has_wifi=int(request.form.get("has_wifi")),
            has_sockets=int(request.form.get("has_sockets")),
            can_take_calls=int(request.form.get("can_take_calls")),
            coffee_price=f'£{request.form.get("coffee_price")}'
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete")
def delete():
    cafe_id = request.args.get('id')
    cafe = Cafe.query.get(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
