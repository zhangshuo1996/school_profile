import os
from config import MYSQL_PRODUCTION_URI, SQLALCHEMY_BINDS

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    # wtform库用于CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', "secret key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 记录查询信息
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_BINDS = SQLALCHEMY_BINDS
    # 数据库连接池的回收时间
    SQLALCHEMY_POOL_RECYCLE = 280
    SLOW_QUERY_THRESHOLD = 1
    # CKEDITOR
    CKEDITOR_SERVE_LOCAL = False
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'activity.upload_image'
    # 文件上传路径
    FILE_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    # 头像上传路径
    AVATAR_UPLOAD_PATH = os.path.join(FILE_UPLOAD_PATH, 'avatar')
    # 模板
    PROJECT_RESULT_TEMPLATE_PATH = os.path.join(FILE_UPLOAD_PATH, 'project_result_template')
    # 专利地图使用的路径
    PATENT_NETWORK_PATH = os.path.join(FILE_UPLOAD_PATH, 'relation_data')

    # 高校画像使用高校图片的路径
    SCHOOL_HEADER_PATH = os.path.join(basedir, "web", "static", "school_profile", "school_header")
    SCHOOL_AVATAR_PATH = os.path.join(basedir, "web", "static", "school_profile", "school_avatar")
    INDUSTRY_LEVEL_LOGO_PATH = os.path.join(basedir, "web", "static", "school_profile", "industry_level_logo")

    # 高校画像保存搜索结果doc文档的路径
    SCHOOL_SEARCH_DOC_PATH = os.path.join(FILE_UPLOAD_PATH, 'school_search_doc')

    ACTIVITY = "ACTIVITY"
    DECLARATION = "DECLARATION"
    POLICY = "POLICY"


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    SQLALCHEMY_DATABASE_URI = MYSQL_PRODUCTION_URI
    port = 8080


class TestingConfig(BaseConfig):
    """测试环境配置"""
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    pass


configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# 中介（孵化器）类型
AGENT_PATTERN = ["官办官营", "官办民营", "民办民营"]

# 中介（孵化器）等级
AGENT_LEVEL = ["", "国家级", "省级", "市级", "县级"]

RELATION = {
    "WRITE": "write",
    "INCLUDE": "include",
    "EMPLOY": "employ",
    "HANDLE": "handle",
    "MANAGE": "manage",
    "LOCATE": "locate",
    "COOPERATE": "cooperate",
    "KNOWS": "knows",  # 中介与专家/工程师的关系
    "PARTNER": "partner",  # 高校中介和地区中介的合作关系
    "INVOLVE": "involve",  # 专家/工程师（团队）所涉及的技术领域 （IPC）
    "PSM": "PSM",  # 专家个人与工程师个人的 相似性预测关系
    "CSM": "CSM"  # 专家团队与工程师团队的 相似性预测关系
}

LABEL = {
    "CITY": "City",
    "TOWN": "Town",
    "UNIVERSITY": "University",
    "TEACHER": "Teacher",
    "COMPANY": "Company",
    "ENGINEER": "Engineer",
    "PATENT": "Patent",
    "IPC": "IPC",
    "TTC": "TechnologyTransferCenter",  # 高校技术转移中心
    "TTP": "TechnologyTransferPlatform",  # 地区技术转移平台
    "areaAGENT": "Agent_Area",  # 地区技术转移中心的中介用户
    "uniAGENT": "Agent_University",  # 高校技术转移中心的中介用户
}