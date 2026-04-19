import os
import json
from config import Config
import dao

VIDEO_DIR = Config.VIDEO_DIR


def scan_and_sync():
    """
    扫描磁盘目录，解析元数据，并同步到数据库。
    返回成功同步的视频数量。
    """
    video_dicts = []

    # 遍历一级目录
    for video_id in os.listdir(VIDEO_DIR):
        video_path = os.path.join(VIDEO_DIR, video_id)
        if not os.path.isdir(video_path):
            continue

        # 遍历二级目录（视频文件）
        for filename in os.listdir(video_path):
            if filename.lower().endswith(".mp4"):
                # 构建数据字典
                video_item = {
                    "name": filename,
                    "video_id": video_id,
                    "title": "",
                    "preview": "",
                }

                # 解析 project.json
                project_json_path = os.path.join(video_path, "project.json")
                try:
                    with open(project_json_path, "r", encoding="utf-8") as f:
                        project_data = json.load(f)
                        video_item["title"] = project_data.get("title", "")
                        video_item["preview"] = project_data.get("preview", "").split(
                            "."
                        )[-1]
                except Exception as e:
                    print(f"[警告] 错误读取 {project_json_path}: {e}")
                video_dicts.append(video_item)

    # 写入数据库
    added_count, deleted_count = dao.refresh_videos(video_dicts)
    return added_count, deleted_count
