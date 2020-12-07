from web.extensions import db
from .relation import user_category_menu


class UserCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), comment='用户类型名称')

    # 反向建立
    menus = db.relationship('Menu', secondary=user_category_menu, backref='user_categories')
    # 类型对应的用户
    users = db.relationship('User')
