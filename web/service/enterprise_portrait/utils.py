"""
文件操作
"""
import os
import uuid
import openpyxl as xl
from flask import send_from_directory

# 文件上传路径
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 文件上传路径
FILE_UPLOAD_PATH = os.path.join(basedir, 'enterprise_portrait', 'uploads')


def random_filename(filename):
    # 处理文件名，防止系统文件被篡改
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def write_ep_excel_file(result, filename, type=1):
    filename = random_filename(filename)
    # 没有文件夹则创建文件夹
    if not os.path.exists(FILE_UPLOAD_PATH):
        os.makedirs(FILE_UPLOAD_PATH)
    result_path = os.path.join(FILE_UPLOAD_PATH, filename + ".xlsx")
    workbook = xl.Workbook()
    workbook.save(result_path)
    sheet = workbook.active
    if type == 1:
        sheet.append(["企业名", "经营状态", "法定代表人", "注册资本", "成立日期", "所属省份", "所属城市", "所属县",
                      "电话", "更多电话", "邮箱", "更多邮箱", "统一社会信用代码", "纳税人识别号", "注册号", "组织机构代码", "参保人數",
                      "企业类型", "所属行业", "曾用名", "网址", "企业地址", "经营范围"])
    else:
        sheet.append(["专利名", "申请号", "申请日", "公开号", "公开日", "申请人", "地址", "发明人", "国审代码", "摘要",
                      "主权项", "主分类号", "专利分类号", "专利代理机构", "专利代理人"])
    for data in result:
        sheet.append(data)
    workbook.save(result_path)
    return filename+".xlsx"


def download_by_path(file_name):
    file_path = os.path.join(FILE_UPLOAD_PATH)
    return send_from_directory(file_path, file_name)