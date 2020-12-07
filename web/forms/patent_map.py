"""
by: xiaoniu
用于验证共分类网络的传递的数据的有效性
"""
from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired,AnyOf


class GraphForm(Form):
    """不用做显示，仅仅用来判断"""
    # 类别，目前必须是school | district
    category = StringField(validators=[DataRequired(), AnyOf(['school', 'district'])])
    unit_name = StringField(validators=[DataRequired()])
    # 非必选项
    class_ = StringField()
    depth = IntegerField()
