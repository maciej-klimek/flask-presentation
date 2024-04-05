from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.models import db, User

bp = Blueprint('login_bp', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()

        # Verify the password if the user exists
        if user and check_password_hash(user.password, password):
            # Store user information in the session
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('notes_bp.notes'))
        else:
            return render_template('login.html', error="Nieprawidłowe hasło lub username.")
    else:
        return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Taki username już istnieje.")

        # Create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login_bp.login'))
    
    # If it's a GET request or if the username already exists
    return render_template('register.html')

@bp.route('/logout')
def logout():
    # Remove user information from the session
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login_bp.login'))
