from models import db, Video
import logging

logger = logging.getLogger(__name__)

def get_all_videos():
    """从数据库获取所有视频，返回字典列表"""
    videos = Video.query.all()
    return [
        {"file": v.file, "video_id": v.video_id, "title": v.title, "preview": v.preview}
        for v in videos
    ]


def refresh_videos(video_dicts):
    added_ids = []
    try:
        # 1. 预先加载：一次性从数据库查出所有现有记录，构建 {video_id: 对象} 的字典
        existing_videos = {v.video_id: v for v in Video.query.all()}

        new_videos = set()

        for item in video_dicts:
            vid = item["video_id"]
            new_videos.add(vid)

            if vid in existing_videos:
                # 2. 记录已存在：直接修改内存中对象的属性
                v = existing_videos[vid]
                v.file = item["file"]
                v.title = item.get("title", "")
                v.preview = item.get("preview", "")
            else:
                # 3. 记录不存在：创建新对象并加入 session
                db.session.add(
                    Video(
                        video_id=vid,
                        file=item["file"],
                        title=item.get("title", ""),
                        preview=item.get("preview", ""),
                    )
                )
                added_ids.append(vid)

        # 4. 删除扫描中已不存在的记录
        deleted_ids = set(existing_videos.keys()) - new_videos
        for vid in deleted_ids:
            db.session.delete(existing_videos[vid])

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    # 记录视频信息增删
    for vid in added_ids:
        logger.info(f"ADD {vid}")
    for vid in deleted_ids:
        logger.info(f"DEL {vid}")

    return len(added_ids), len(deleted_ids)
