from models import db, Video, Scene
import logging
from config import Config
import subprocess
import glob
import os
import shutil

logger = logging.getLogger(__name__)

def get_all_videos():
    """从数据库获取所有视频，返回字典列表"""
    videos = Video.query.all()
    return [
        {"file": v.file, "video_id": v.video_id, "title": v.title, "preview": v.preview}
        for v in videos
    ]

def get_all_scenes():
    """从数据库获取所有场景，返回字典列表"""
    scenes = Scene.query.all()
    return [
        {
            "scene_id": s.scene_id,
            "title": s.title,
            "preview": s.preview,
        }
        for s in scenes
    ]

def get_pictures_by_scene_id(scene_id):
    """获取场景图片列表"""
    scene = Scene.query.filter_by(scene_id=scene_id).first()
    if not scene:
        return []
    return [img.image_name for img in scene.images]

def refresh_videos(video_dicts):
    added_ids = []
    try:
        # 预先加载：一次性从数据库查出所有现有记录，构建 {video_id: 对象} 的字典
        existing_videos = {v.video_id: v for v in Video.query.all()}

        new_videos = set()

        for item in video_dicts:
            vid = item["video_id"]
            new_videos.add(vid)

            if vid not in existing_videos:
                # 记录不存在：创建新对象并加入 session
                db.session.add(
                    Video(
                        video_id=vid,
                        file=item["file"],
                        title=item.get("title", ""),
                        preview=item.get("preview", ""),
                    )
                )
                added_ids.append(vid)

        # 删除扫描中已不存在的记录
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

def refresh_scenes(scene_dicts):
    added_ids = []
    try:
        existing_scenes = {s.scene_id: s for s in Scene.query.all()}
        new_scenes = set()

        for item in scene_dicts:
            sid = item["scene_id"]
            new_scenes.add(sid)

            # 处理新增记录
            if sid not in existing_scenes:
                s = Scene(
                    scene_id=sid,
                    title=item.get("title", ""),
                    preview=item.get("preview", ""),
                )
                db.session.add(s)
                added_ids.append(sid)

        # 删除扫描中已不存在的记录
        deleted_ids = set(existing_scenes.keys()) - new_scenes
        for sid in deleted_ids:
            db.session.delete(existing_scenes[sid])

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    for sid in added_ids:
        logger.info(f"ADD {sid}")
    for sid in deleted_ids:
        logger.info(f"DEL {sid}")

    return len(added_ids), len(deleted_ids)


def scene2picture_temp(scene_id):
    r"""
    将场景转换为图片。
    返回图片路径。
    步骤1：先清空temp路径，再将文件写入temp目录

    步骤2：工具提取
    命令：`..\..\tools\RePKG.exe extract -e tex -s -o ..\..\temp\scenes\<scene_id> "C:\Program Files (x86)\steam\steamapps\workshop\content\431960\<scene_id>\scene.pkg"`
    步骤2：删除无用文件
    在\temp\scenes\<scene_id>目录下删除['.tex','.tex-json']后缀的文件
    步骤3：统计
    返回剩下的文件名列表
    """
    # 确保 scene_id 为字符串
    scene_id = str(scene_id)
    
    # 获取项目根目录
    base_dir = Config.BASE_DIR
    # 构建各路径
    repkg_exe = os.path.join(base_dir, 'tools', 'RePKG', 'RePKG.exe')
    workshop_scene_path = os.path.join(Config.WALLPAPER_DIR, scene_id, 'scene.pkg')
    temp_dir = os.path.join(base_dir, 'temp', 'scenes')
    output_dir = os.path.join(temp_dir, scene_id)

    # 清空输出目录
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logger.info("清空输出目录")
    
    # 步骤1：提取纹理文件
    cmd = [
        repkg_exe,
        'extract',
        '-e', 'tex',
        '-s',
        '-o', output_dir,
        workshop_scene_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"RePKG 提取失败: {e.stderr}")
        return ""
    except FileNotFoundError:
        logger.error(f"RePKG 工具未找到: {repkg_exe}")
        return ""
    
    # 步骤2：删除 .tex 和 .tex-json 文件
    for ext in ['*.tex', '*.tex-json']:
        pattern = os.path.join(output_dir, ext)
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
            except OSError as e:
                logger.error(f"删除文件失败 {file_path}: {e}")
    
    # 步骤3：获取剩余图片文件名
    try:
        files = [f for f in os.listdir(output_dir) 
                 if os.path.isfile(os.path.join(output_dir, f))]
    except FileNotFoundError:
        logger.error(f"输出目录不存在: {output_dir}")
        return []
    
    # 返回文件名列表
    return files
