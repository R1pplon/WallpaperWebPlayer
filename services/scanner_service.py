import os
import json
from config import Config
import dao

WALLPAPER_DIR = Config.WALLPAPER_DIR


def video_scan_and_sync():
    """
    扫描磁盘目录，解析元数据，并同步到数据库。
    返回成功同步的视频数量。
    """
    video_dicts = []

    # 遍历目录
    for video_id in os.listdir(WALLPAPER_DIR):
        video_path = os.path.join(WALLPAPER_DIR, video_id)
        if not os.path.isdir(video_path):
            continue

        # 解析 project.json
        project_json_path = os.path.join(video_path, "project.json")
        try:
            with open(project_json_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)
                if project_data.get("type", "").lower() == "video":
                    video_dicts.append({
                        "video_id": video_id,
                        "file": project_data.get("file", ""),
                        "title": project_data.get("title", ""),
                        "preview": project_data.get("preview", ""),
                    })
        except FileNotFoundError:
            # 文件不存在，直接跳过
            pass
        except Exception as e:
            print(f"[警告] 错误读取 {project_json_path}: {e}")
        
    # 写入数据库
    added_count, deleted_count = dao.refresh_videos(video_dicts)

    return added_count, deleted_count
