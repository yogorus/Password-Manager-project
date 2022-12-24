from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EncryptedType, StringEncryptedType
import validators
from datetime import datetime

from helpers import login_required, apology
from crypto import load_key

KEY = load_key()


app = Flask(__name__)
app.app_context().push()

app.config['DEBUG'] = True
app.debug = True
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SECRET_KEY'] = 'yourcodehere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db = SQLAlchemy(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    passwords = db.relationship('Password', backref='passwords', lazy=True)

    def __init__(self, username, password):
        self.username = username.strip()
        self.hash = generate_password_hash(password.strip())
        
    def __repr__(self):
        return f'id: {self.id}, username: {self.username},\nhash {self.hash}'


class Password(db.Model):
    __tablename__ = "passwords"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    link = db.Column(db.String, nullable=True) 
    password = db.Column(StringEncryptedType(db.String, KEY), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, title, link, password, description, user_id):
        self.title = title
        self.password = password
        self.link = link
        self.description = description
        self.user_id = user_id
        
    
    def __repr__(self):
        return f'password_id: {self.id}, title: {self.title},\nlink: {self.link}\npassword: {self.password}\ndescription:\n{self.description},\nuser_id: {self.user_id}, \n{self.date}'



@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    # Edit or Delete
    if request.method == 'POST':
        """Delete password from the database"""
        if request.form.get('btn') == 'Delete':
            id = request.form.get('id')
            
            if id:
                # Validate
                password_to_delete = Password.query.filter_by(id=id).first_or_404()

                try:
                    db.session.delete(password_to_delete)
                    db.session.commit()
                    flash(f'{password_to_delete.title} Deleted!')
                    return redirect('/')
                except:
                    return 'Something went wrong with deleting that password...'
        
    
    """Return all the password items for that user"""
    if request.method == 'GET':
       return render_template('index.html')


@app.route('/search')
@login_required
def search():
    q = request.args.get('q')
    if q:
        passwords = Password.query.filter(Password.user_id==session['user_id'], Password.title.like(f'%{q}%')).order_by(Password.date.desc()).all()
    else:   
        passwords = Password.query.filter_by(user_id=session["user_id"]).order_by(Password.date.desc()).all()

    # Convert datetime into a human-friendly format
    for item in passwords:
        item.date = item.date.strftime("%d-%m-%Y %H:%M:%S")
    return render_template('search.html', passwords=passwords)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit password item"""
    item = Password.query.filter_by(id=id).first_or_404()

    if request.method == 'POST':
        
        # Validate input fields
        title = request.form.get('title').strip()
        link = request.form.get('link').strip()
        password = request.form.get('password').strip()
        description = request.form.get('description').strip()
        
        # Validate title
        if not title:
            return apology("must provide title", 400)
        
        # Validate password
        elif not password:
            return apology('must prove password', 400)

        # Validate link
        if link:
            if not validators.url(link):
                return apology("Invalid link format!", 400)
        
        # Update db
        try:
            item.title = title
            item.link = link
            item.password = password
            item.description = description
            db.session.commit()
            flash('Edited!')
            return redirect('/')

        except:
            return 'There was a problem editing that password'

    else:
        if session["user_id"] != item.user_id:
            return apology('Restricted password id for that user', 403)

        return render_template('edit.html', item=item)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username").strip()).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.hash, request.form.get("password").strip()):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        flash("Logged in!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == 'POST':

        # Check for submission
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Check if username already exists
        user = User.query.filter_by(username=request.form.get("username").strip()).first()
        if user:
            return apology("Username already exists", 400)

        # Check for password
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Check for confirmation
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation does not match", 400)

        # Add new account to the database
        user = User(request.form.get("username"), request.form.get("password"))
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username=request.form.get("username").strip()).first()

        # Start session
        session["user_id"] = user.id

        # Redirect to homepage
        flash("Registred!")
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add child password to db"""
    if request.method == 'POST':
        # Validate input fields
        title = request.form.get('title').strip()
        link = request.form.get('link').strip()
        password = request.form.get('password').strip()
        description = request.form.get('description').strip()
        
        # Validate title
        if not title:
            return apology("must provide title", 400)
        
        # Validate password
        elif not password:
            return apology('must prove password', 400)

        # Validate link
        if link:
            if not validators.url(link):
                return apology("Invalid link format!", 400)
        
        # Add new item to database
        item = Password(title, link, password, description, session["user_id"])
        db.session.add(item)
        db.session.commit()

        flash('Password Added!')
        return render_template('add.html')


    # Render form via GET
    else:
        return render_template('add.html')


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """ Change user master password """
    if request.method == "POST":

        user = User.query.filter_by(id=session["user_id"]).first()
        # Ensure password was submitted
        if not request.form.get("old_password"):
            return apology("must provide password", 400)

        # Check if the password is correct
        elif not check_password_hash(user.hash, request.form.get("old_password")):
            return apology("invalid password", 400)

        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        elif request.form.get("confirmation") != request.form.get("new_password"):
            return apology("password and confirmation does not match", 400)

        # Change password
        user.hash = generate_password_hash(request.form.get("new_password"))
        db.session.commit()

        flash("Password succesfully changed!")
        return redirect("/")

    else:
        return render_template("change.html")


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=8000
            )
