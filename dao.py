from models import db, Video


def get_all_videos():
    """从数据库获取所有视频，返回字典列表"""
    videos = Video.query.all()
    return [
        {"name": v.name, "video_id": v.video_id, "title": v.title, "preview": v.preview}
        for v in videos
    ]


def refresh_videos(video_dicts):
    try:
        # 1. 预先加载：一次性从数据库查出所有现有记录，构建 {video_id: 对象} 的字典
        existing_videos = {v.video_id: v for v in Video.query.all()}

        new_videos = set()
        added_count = 0

        for item in video_dicts:
            vid = item["video_id"]
            new_videos.add(vid)

            if vid in existing_videos:
                # 2. 记录已存在：直接修改内存中对象的属性
                v = existing_videos[vid]
                v.name = item["name"]
                v.title = item.get("title", "")
                v.preview = item.get("preview", "")
            else:
                # 3. 记录不存在：创建新对象并加入 session
                db.session.add(
                    Video(
                        video_id=vid,
                        name=item["name"],
                        title=item.get("title", ""),
                        preview=item.get("preview", ""),
                    )
                )
                added_count += 1

        # 4. 删除扫描中已不存在的记录
        deleted_count = Video.query.filter(~Video.video_id.in_(new_videos)).delete(
            synchronize_session=False
        )

        db.session.commit()
        # return len(video_dicts)
        return added_count, deleted_count
    except Exception as e:
        db.session.rollback()
        print(f"数据库更新失败: {e}")
        return 0
