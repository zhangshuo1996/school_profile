from web.extensions import db


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), comment='菜单名')
    endpoint = db.Column(db.String(64), comment='链接')
    icon = db.Column(db.String(24), comment='图标')
    sequence = db.Column(db.Integer, default=0, comment='顺序')
    parent_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    # 邻接列表
    parent = db.relationship('Menu', back_populates='sub_menu', remote_side=[id])
    sub_menu = db.relationship('Menu', back_populates='parent', uselist=False, cascade='all')

    @property
    def blueprint(self):
        """从endpoint获取蓝图"""
        array = self.endpoint.split('.')
        return array[0]
