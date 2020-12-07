from web.extensions import db
from web.models.data_mining.district import District


class CoclassificationNetwork(db.Model):
    """共分类网络"""
    __bind_key__ = 'data_mining'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nodes = db.Column(db.JSON)
    links = db.Column(db.JSON)
    communities = db.Column(db.JSON)
    unit_id = db.Column(db.Integer, comment='单位id district_id或school_id')
    category = db.Column(db.Enum('district', 'school'), comment='district或者school', nullable=False)

    @staticmethod
    def get_network(category, unit_name):
        """
        根据category和unit_name获取对应的共分类网络
        :param category: district | school
        :param unit_name: town | school_name
        :return: None | CoclassificationNetwork
        """
        unit_id = None
        if category == 'district':
            district = District.query.filter_by(town=unit_name).first()
            unit_id = district.id
        if unit_id is None:
            return
        network = CoclassificationNetwork.query.filter_by(unit_id=unit_id, category=category).first()
        return network
