from wtforms.validators import ValidationError


def date_picker(form, filed):
    """判断file是否满足date picker"""
    if len(filed.data) == 0:
        raise ValidationError('日期格式错误')
