"""
文件上传，下载相关
by zhang
"""
import os
from flask_login import login_required, current_user
from flask import Blueprint, request, flash, send_from_directory, current_app

from web.extensions import db
from web.models import UploadFile
from web.utils.url import redirect_back
from web.forms import UploadFileForm

file_bp = Blueprint("file", __name__)


@file_bp.route("/upload_file", methods=["POST"])
@login_required
def upload_file():
    """
    上传文件,
    给定上传的参数时加上上传文件的类型：
    文件类型，1：申报项目，2：活动，3：政策，4：合同
    """
    form = UploadFileForm(request.form)
    ret = False
    if form.validate_on_submit():
        ret = form.add_file(current_user.name)
    if not ret:
        flash('文件上传出错，请稍后重试', 'danger')
    return redirect_back()


@file_bp.route("/download_file/<file_id>")
@login_required
def download_file(file_id):
    """
    下载文件
    :param file_id: 文件id
    :return:
    """
    file_obj = UploadFile.query.get(file_id)
    path = file_obj.path
    filename_hash = file_obj.filename_hash
    file_path = os.path.join(current_app.config['FILE_UPLOAD_PATH'], path)
    return send_from_directory(file_path, filename_hash, as_attachment=True, attachment_filename=file_obj.filename)


@file_bp.route("/delete_file", methods=['POST'])
@login_required
def delete_file():
    """
    根据file_id完全删除的数据库中的文件记录以及文件系统中的文件
    :return:
    """
    file_id = request.form.get("file_id", default=None, type=int)
    try:
        file_obj = UploadFile.query.get(file_id)
        db.session.delete(file_obj)
        db.session.commit()
        flash('操作成功', 'success')
    except Exception as e:
        print(e)
        flash('操作失败', 'danger')
    return redirect_back()
