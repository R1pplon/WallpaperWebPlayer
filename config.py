import os

# 获取当前文件所在目录的绝对路径，作为项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 视频文件根目录
    VIDEO_DIR = "/run/media/r1pple/Win10Pro/Program Files (x86)/steam/steamapps/workshop/content/431960"

    # --- 数据库配置 ---
    SQLITE_DB_PATH = os.path.join(BASE_DIR, "videos.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLITE_DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    DEBUG = True
