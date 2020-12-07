from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_moment import Moment


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
moment = Moment()

login_manager.login_view = 'auth.login'
login_manager.session_protection = 'basic'
login_manager.login_message = None
login_manager.login_message_category = None


@login_manager.user_loader
def load_user(user_id):
    from web.models import User
    user = User.query.get(user_id)
    return user
