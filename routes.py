import os
from flask import Blueprint, render_template, send_from_directory, current_app

import dao
from services import scanner_service

bp = Blueprint("main", __name__)


@bp.route("/videos")
def videos():
    """视频列表页"""
    videos = dao.get_all_videos()
    return render_template("videos.html", videos=videos)


@bp.route("/video/<path:video_path>")
def video_player(video_path):
    """视频播放页"""
    return render_template("video.html", video_path=video_path)


@bp.route("/videos/<path:filename>")
def serve_video(filename):
    """提供视频文件流"""
    WALLPAPER_DIR = current_app.config["WALLPAPER_DIR"]
    return send_from_directory(WALLPAPER_DIR, filename)


@bp.route("/preview/<id>/<filename>")
def serve_preview(id, filename):
    """提供封面图片"""
    WALLPAPER_DIR = current_app.config["WALLPAPER_DIR"]
    return send_from_directory(os.path.join(WALLPAPER_DIR, id), filename)


@bp.route("/update")
def manual_update():
    """手动触发扫描同步"""
    added_count, deleted_count = scanner_service.all_scan_and_sync()
    return f"扫描完成，新增 {added_count} 个壁纸，删除 {deleted_count}个壁纸"


@bp.route("/scenes")
def scenes():
    """场景列表页"""
    scenes = dao.get_all_scenes()
    return render_template("scenes.html", scenes=scenes)

@bp.route("/scene/<id>")
def scenes_picture_list(id):
    """根据场景ID获取图片列表"""
    picture_list = dao.get_pictures_by_scene_id(id)
    return render_template("scene.html", id=id, pictures=picture_list)

@bp.route("/scenes/<id>/<filename>")
def scenes_picture(id, filename):
    """提供场景图片"""
    PICTURE_DIR = current_app.config["PICTURE_DIR"]
    return send_from_directory(os.path.join(PICTURE_DIR, id), filename)