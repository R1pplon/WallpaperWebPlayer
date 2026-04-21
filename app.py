from flask import Flask
from config import Config
from models import db
from routes import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(bp)
    return app


if __name__ == "__main__":
    import dao
    from services import scanner_service

    app = create_app()

    with app.app_context():
        db.create_all()

        # 启动时检查，如果数据库没数据，自动执行一次全量扫描
        if not dao.get_all_videos():
            print("检测到数据库为空，执行首次扫描...")
            added_count, deleted_count = scanner_service.video_scan_and_sync()
            print(
                f"首次扫描完成，新增 {added_count} 个视频，删除 {deleted_count} 个视频"
            )

    print(f"视频目录: {app.config['WALLPAPER_DIR']}")
    app.run(host="0.0.0.0", port=58763)
