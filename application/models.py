from application import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Account.query.get(int(id))

#Creating required database models

class Account(db.Model, UserMixin):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String(40), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    phones = db.relationship('Phone', backref='account', lazy=True)

    def __repr__(self):
        return f"Account('{self.id}', '{self.auth_id}', '{self.username}')"


class Phone(db.Model):
    __tablename__ = "phone_number"
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(40), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    
    def __repr__(self):
        return f"Phone('{self.number}', '{self.account_id}')"  