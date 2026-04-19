import os
from flask import Blueprint, render_template, send_from_directory, current_app

import dao
from services import scanner_service

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """视频列表页"""
    videos = dao.get_all_videos()
    return render_template("index.html", videos=videos)


@bp.route("/video/<path:video_path>")
def video_player(video_path):
    """视频播放页"""
    return render_template("video.html", video_path=video_path)


@bp.route("/videos/<path:filename>")
def serve_video(filename):
    """提供视频文件流"""
    video_dir = current_app.config["VIDEO_DIR"]
    return send_from_directory(video_dir, filename)


@bp.route("/preview/<video_id>/<filename>")
def serve_preview(video_id, filename):
    """提供封面图片"""
    video_dir = current_app.config["VIDEO_DIR"]
    return send_from_directory(os.path.join(video_dir, video_id), filename)


@bp.route("/update")
def manual_update():
    """手动触发扫描同步"""
    added_count, deleted_count = scanner_service.scan_and_sync()
    return f"首次扫描完成，新增 {added_count} 个视频，删除 {deleted_count}个视频"
