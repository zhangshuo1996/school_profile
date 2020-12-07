import os
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for, abort


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    # 获取用户的所有菜单
    menus = current_user.category.menus
    # TODO：对菜单进行排序
    menus = sorted(menus, key= lambda x: x.sequence)
    # 遍历菜单
    for menu in menus:
        # 该菜单有子菜单
        if menu.sub_menu and menu.sub_menu.name == 'ROLE':
            # 用户未对应任何department，跳过
            departments = current_user.get_departments()
            if len(departments) == 0:
                continue
            return redirect(url_for(menu.sub_menu.endpoint, department_id=departments[0].id))
        else:
            return redirect(url_for(menu.endpoint))
