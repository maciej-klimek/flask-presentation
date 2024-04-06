from flask import Flask
from models.models import db
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.secret_key = "fdasjghfkzrytsadhfgkjas"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

csrf = CSRFProtect(app)



from views.login import bp as bp_login
app.register_blueprint(bp_login)

from views.notes import bp as bp_notes
app.register_blueprint(bp_notes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)