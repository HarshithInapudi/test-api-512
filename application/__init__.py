from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import redis

app = Flask(__name__)

# app.config.from_pyfile(config_file)

app.config['SECRET_KEY'] = 'eeabd520b0cb29de98c98f740ee13b0a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://viqgkicktvipwn:203e2abde62e4839e983d595a545701d2ee48fbe97e06f0a353013afcd28ae69@ec2-54-247-71-245.eu-west-1.compute.amazonaws.com:5432/db8vb2iocjc3j7'

r = redis.from_url('redis://h:pd92d2438fafc8ab8a9aca11a05291cdaddd1a4e133279d8f87ddf2ccaadcb336@ec2-52-215-86-130.eu-west-1.compute.amazonaws.com:31669')


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



from application import routes