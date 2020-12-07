import xlrd
from web.models.project_result import ProjectResult
from web.extensions import db


def upload_namelist(namelist_file, uploader, gmt_create, project_id):
    f = namelist_file.read()
    excel = xlrd.open_workbook(file_contents=f)
    # Book(工作簿)对象方法
    all_sheet = excel.sheets()
    for sheet in all_sheet:
        # 循环遍历每一行
        for each_row in range(sheet.nrows):
            each_row_list = sheet.row_values(each_row)
            ep_name = each_row_list[0]
            remarks = each_row_list[1]
            year = each_row_list[2]
            project_result = ProjectResult(ep_name=ep_name, remarks=remarks, year=year, uploader=uploader,
                                           gmt_create=gmt_create,
                                           project_id=project_id)
            db.session.add(project_result)
        db.session.commit()
        break
