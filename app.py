from flask import Flask
from config import Config
from models import db
from routes import bp
import os
import sys
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(bp)
    return app


def run_startup_checks(app):
    """启动前的环境与数据检查"""
    logger = logging.getLogger(__name__)

    if not os.path.exists(app.config["WALLPAPER_DIR"]):
        logger.error(
            f"视频目录不存在 '{app.config['WALLPAPER_DIR']}'，请检查配置后重试。"
        )
        sys.exit(1)

    if not dao.get_all_videos():
        logger.info("检测到数据库为空，执行首次扫描...")
        added_count, _ = (
            scanner_service.all_scan_and_sync()
        )
        if added_count == 0:
            logger.error("未找到壁纸信息，请检查配置后重试。")
            sys.exit(1)
        logger.info(f"首次扫描完成，新增 {added_count} 个视频")


if __name__ == "__main__":
    import dao
    from services import scanner_service

    # 日志规则
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(Config.LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)

    app = create_app()

    with app.app_context():
        db.create_all()
        run_startup_checks(app)

    logger.info(f"视频目录: {app.config['WALLPAPER_DIR']}")
    app.run(host="0.0.0.0", port=58763)
