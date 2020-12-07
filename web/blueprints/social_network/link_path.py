from flask import Blueprint, render_template, request
from web.service.social_network import link_path as path_service

link_path_bp = Blueprint('link_path', __name__)


@link_path_bp.route("/path")
def getLinkPath():
    # TODO 待获取数据，
    agent_id = 123  # 从登陆信息中获取
    agent_type = "uni"  # 从登陆信息中获取
    target_id = request.args.get("target", default=0, type=int)
    target_type = request.args.get("t_type", default="teacher", type=str)
    step = request.args.get("step", default=3, type=int)
    limit = request.args.get("limit", default=5, type=int)

    return path_service.getLinkPath(agent_id=1, agent_type="uni", target_id=4862608, target_type="teacher", max_step=3,
                                    limit=limit)
