import os
import logging
from datetime import datetime
from flask.logging import default_handler
from flask import Flask, render_template, current_app, url_for, request
from flask_sqlalchemy import get_debug_queries
from logging.handlers import RotatingFileHandler

from web.blueprints.admin.admin_auth import admin_auth_bp
from web.settings import configuration
from web.blueprints import main_bp, auth_bp, project_declaration_bp, file_bp
from web.blueprints.enterprise_portrait.ep_portrait import enterprise_portrait_bp
from web.blueprints.patent_map import patent_network_bp
from web.blueprints.project_declaration.ajax import project_declaration_ajax_bp
from web.blueprints.project_declaration.project_declaration import project_declaration_bp

from web.blueprints.user.user import user_bp
from web.blueprints import main_bp, auth_bp, activity_bp, statistic_input_bp
from web.blueprints.wechat_public_platform.wx_public_platform import wx_public_platform_bp

from web.blueprints import main_bp, auth_bp, activity_bp, user_bp, storage_bp, system_bp, statistics_bp, gov_bp, agent_bp


# 工程师社区
from web.blueprints.engineeer_community.engineer_community import engineer_community_bp
from web.blueprints.school_profile import school_search_bp
from web.blueprints.school_profile import school_profile_bp

# 校企合作相关
from web.blueprints.social_network.recommend import recommend_bp as recommend_bp
from web.blueprints.social_network.recommend_graph import recommend_graph_bp as recommend_graph_bp
from web.blueprints.social_network.link_path import link_path_bp as link_path_bp

from web.extensions import db, bootstrap, login_manager, csrf, ckeditor, moment
from web.models import User, Role, Permission, Menu, UserCategory, Agent, ServiceProvider, ServiceProviderCategory
from web.models import TechnicalRequirement, UploadFile, Activity
from web.models import ProjectDeclaration, Enterprise, ProjectTaskTemplate, Project, Department, ProjectDeclarationTask


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', "development")

    app = Flask('web')
    app.config.from_object(configuration[config_name])

    # 注册日志处理器
    register_logging(app)
    # 初始化扩展
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)
    # 注册自定义shell命令
    register_commands(app)
    # 注册错误处理函数
    register_errors(app)
    # 注册shell
    register_shell_context(app)
    # 注册模板上下文处理函数
    register_template_context(app)
    register_template_filter(app)
    register_request_handlers(app)

    return app


def register_logging(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler('logs/log.txt', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    default_handler.setLevel(logging.INFO)
    # 在调试状态下不会添加处理器
    if not app.debug:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(default_handler)


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= current_app.config['SLOW_QUERY_THRESHOLD']:
                current_app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s Query:%s\n'
                    % (q.duration, q.context, q.statement)
                )
        return response


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(project_declaration_bp, url_prefix='/project_declaration')
    app.register_blueprint(project_declaration_ajax_bp, url_prefix='/project_declaration/ajax')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(activity_bp, url_prefix='/activity')
    app.register_blueprint(file_bp, url_prefix='/file')
    app.register_blueprint(wx_public_platform_bp, url_prefix='/wechat_public_platform')
    app.register_blueprint(storage_bp, url_prefix='/storage')
    app.register_blueprint(statistics_bp, url_prefix='/statistics')
    # 统计输入相关
    app.register_blueprint(statistic_input_bp, url_prefix='/statistics/input')
    # 工程师社区
    app.register_blueprint(engineer_community_bp, url_prefix='/engineer_community')

    # 后台管理模块
    app.register_blueprint(admin_auth_bp, url_prefix='/admin/auth')
    app.register_blueprint(system_bp, url_prefix='/admin/system')
    app.register_blueprint(gov_bp, url_prefix='/admin/gov')
    app.register_blueprint(agent_bp, url_prefix='/admin/agent')
    # 企业画像相关
    app.register_blueprint(enterprise_portrait_bp, url_prefix='/data_mining/enterprise_portrait')
    # 专利地图相关
    app.register_blueprint(patent_network_bp, url_prefix='/data_mining/patent_map')

    # 高校画像模块
    app.register_blueprint(school_profile_bp, url_prefix='/school/profile')
    app.register_blueprint(school_search_bp, url_prefix='/school/search')

    # 校企合作相关
    app.register_blueprint(recommend_bp, url_prefix="/recommend")
    app.register_blueprint(recommend_graph_bp, url_prefix="/recommend-graph")
    app.register_blueprint(link_path_bp, url_prefix="/link-path")


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role, Permission=Permission, Menu=Menu,
                    UserCategory=UserCategory, Agent=Agent, ServiceProvider=ServiceProvider,
                    ServiceProviderCategory=ServiceProviderCategory, TechnicalRequirement=TechnicalRequirement,
                    UploadFile=UploadFile, Activity=Activity, ProjectDeclarationTask=ProjectDeclarationTask,
                    ProjectDeclaration=ProjectDeclaration, Enterprise=Enterprise,
                    Project=Project, ProjectTaskTemplate=ProjectTaskTemplate, Department=Department)


def register_template_context(app):
    """注册模板上下文，使得变量可以在模板中使用"""
    @app.context_processor
    def make_template_context():
        return dict(datetime=datetime)

    @app.template_test()
    def suffix_match(request_url, url):
        """验证后缀是否相同"""
        return request_url.endswith(url)

    @app.template_filter()
    def postfix(filename):
        """返回文件扩展名"""
        after = filename.split('.')[-1]
        image_postfix = ['png', 'jpg', 'jpeg', 'gif']
        if after.lower() in image_postfix:
            return 'img'
        return after

    @app.template_filter()
    def sorted_menus(menus):
        """菜单按照sequence排序"""
        menus = sorted(menus, key=lambda x: x.sequence)
        return menus

    @app.template_filter()
    def combine_start_end_time(gmt_start, gmt_end):
        start_time, end_time = datetime.fromtimestamp(gmt_start), datetime.fromtimestamp(gmt_end)
        # 在同一天
        if start_time.year == end_time.year and start_time.month == end_time.month and start_time.day == end_time.day:
            start_str = start_time.strftime('%Y-%m-%d %H:%M')
            end_str = end_time.strftime('%H:%M')
        else:
            start_str = start_time.strftime('%Y-%m-%d %H:%M')
            end_str = end_time.strftime('%Y-%m-%d %H:%M')
        return '{}~{}'.format(start_str, end_str)

    @app.template_filter("timestamp2date")
    def timestamp2date(s):
        return datetime.fromtimestamp(s).strftime("%Y-%m-%d")

    @app.context_processor
    def inject_url():
        return {
            'url_for': dated_url_for
        }


def register_template_filter(app):
    """注册模板过滤器"""
    pass


def register_errors(app):
    @app.errorhandler(404)
    def bad_request(error):
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(500)
    def bad_request(error):
        print(error)
        # 处理异步请求
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return {"error": True, "errorMsg": "操作失败,请联系管理员"}
        # 处理同步请求
        else:
            return render_template('errors/404.html', error_title="500 error",
                                   error_code="500 error", error="服务器错误，请联系管理员"), 500


def register_commands(app):
    pass


def dated_url_for(endpoint, **kwargs):
    filename = None
    if endpoint == 'static':
        filename = kwargs.get('filename', None)
    if filename:
        input_path = os.path.join(current_app.root_path, endpoint, filename)
        if os.path.exists(input_path):
            kwargs['v'] = int(os.stat(input_path).st_mtime)
    return url_for(endpoint, **kwargs)
