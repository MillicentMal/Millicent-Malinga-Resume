from datetime import datetime
from flask import Flask, request, flash, session, render_template, url_for, redirect
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.datastructures import auth_property
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.core import BooleanField
from flask_wtf import FlaskForm
from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    name  =  db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(80))
    services = db.Column(db.String(10))
    location = db.Column(db.String(30))
    phone = db.Column(db.Integer, nullable=False)
    salon = db.Column(db.String(30))
    ratings = db.Column(db.Integer)
    products = db.relationship('Product', backref='seller', lazy=True)


# Product Class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False )
    price = db.Column(db.String(10), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(256))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    seller_or_not = db.Column(db.String(10))


    
  
class LoginForm(Form):
    email = StringField('Email', validators=[validators.InputRequired()])
    username = StringField('username', validators=[validators.InputRequired(), validators.Length(min=4, max=15)])
    password = PasswordField('password', validators=[validators.InputRequired(), validators.length(min=8, max=80)])
# Registration form for new User
class Registration(Form):
    name = StringField(u'Name', validators=[validators.input_required(), validators.Length(min=1, max=50)])
    username = StringField(u'Username', validators=[validators.input_required()])
    email = StringField('Email', validators=[validators.input_required()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField("Confirm Password")
    seller_or_not = BooleanField("Seller")

# registering to become new user

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Registration(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, seller_or_not=form.seller_or_not.data)
        if new_user.seller_or_not == 1:
            db.session.add(new_user)
            db.session.commit()
            return render_template('login.html')
        else:    
            db.session.add(new_user)
            db.session.commit()
            return render_template("index.html")
    else:
        return render_template('register.html', form=form)





@app.route('/')
def index():
        return render_template('index.html')


@app.route('/about', methods=[ 'GET'])
def about():
    if request.method == 'GET':
        return render_template('about.html')

    
@app.route('/sellers', methods=['POST', 'GET'])
def sellers():
    if request.method == "POST":
        new_product = Product(request.form['name', 'price', 'description', 'image'])
        try:
           db.session.add(new_product)
           db.session.commit()
           return redirect('/sellers')
        except:
            return "There was an issue adding your product"
    else:
        products = Product.query.filter(Product.seller_id).order_by(Product.date_created).all()   
        return render_template("sellers.html", products=products)

# @app.route('/delete/<int:id>')
# def delete(id):
#     product_to_delete = Product.query.get_or_404(id)


#     try:
#         db.session.delete()
#         db.session.commit()
#         return redirect('/')
    
#     except:
#         return "There was a problem with that delete"

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == "POST":
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "There was an issue with your request"
#     else:
#         return render_template('update.html', task=task )

#     else:
#         products = Product.query.filter_by(seller_id=Product.seller_id).all()
#         return render_template("sellers.html", products=products)


# @app.route('/sellers')
# def sellers():
#     return render_template("sellers.html")
if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)