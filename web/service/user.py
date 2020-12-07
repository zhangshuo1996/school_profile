from web.utils.file import save_file


def update_agent_avatar(dirname, avatar_file):
    """上传头像"""
    if avatar_file is None:
        return {"error": False}
    avatar = save_file(dirname, avatar_file)
    return avatar
