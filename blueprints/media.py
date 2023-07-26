from flask import Blueprint, current_app
import os

bp = Blueprint("media",__name__,url_prefix="/media")


@bp.get("/<path:filename>")#可匹配任何文件名
def media_file(filename):
  return os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"),filename)#返回指定图片文件的完整路径，
  # current_app.config.get("UPLOAD_IMAGE_PATH")返回的是图片文件的完整路径+filename文件名