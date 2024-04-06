from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required,roles_required, login_user, LoginForm, RegisterForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt'
db = SQLAlchemy(app)

# Definicja modelu użytkownika
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class ExtendedRegisterForm(RegisterForm):
    email = StringField('Email', [InputRequired(), Length(max=255), Email()])
    password = PasswordField('Password', [InputRequired(), Length(min=6)])


class ExtendedLoginForm(LoginForm):
    email = StringField('Email', [InputRequired(), Length(max=255), Email()])
    password = PasswordField('Password', [InputRequired()])


# Inicjalizacja Flask-Security
with app.app_context():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)

# Strona główna wymagająca logowania
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_datastore.create_user(email=email, password=password)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/admin')
@login_required
@roles_required('admin')
def admin_panel():
    return "Welcome to admin panel"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




