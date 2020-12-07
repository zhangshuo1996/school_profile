from web.extensions import db

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                     )

role_permission = db.Table('role_permission',
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True),
                           )

user_category_menu = db.Table('user_category_menu',
                              db.Column('user_category_id', db.Integer, db.ForeignKey('user_category.id'), primary_key=True),
                              db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
                              )
