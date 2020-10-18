from datetime import datetime
from flask_lenddirect import database, login_manager
from flask_login import UserMixin

INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model,UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    userName = database.Column(database.String(20), unique=True, nullable=False)
    emailId = database.Column(database.String(120), unique=True, nullable=False)
    # profilePic = database.Column(database.String(20), nullable=False, default='profile.png')
    password = database.Column(database.String(60), nullable=False)
    todos = database.relationship('Todos', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.userName}', '{self.emailId}', '{self.todos}')"


class Todos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    date_created = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    # due_date=database.Column(datetime.strptime(due_date, INCOMING_DATE_FMT)) if due_date else None,
    description = database.Column(database.Text, nullable=False)
    completed=database.Column(database.Boolean, nullable=False,default=False )
    priority = database.Column(database.String(100),nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    updated_on = database.Column(database.DateTime, onupdate=datetime.utcnow)
    def __repr__(self):
        return f"Todos('{self.name}', '{self.date_created}')"

