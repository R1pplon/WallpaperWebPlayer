import os

# 获取当前文件所在目录的绝对路径，作为项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    BASE_DIR = BASE_DIR
    # 壁纸文件目录
    WALLPAPER_DIR = "C:/Program Files (x86)/steam/steamapps/workshop/content/431960/"

    # 本地场景图片目录
    PICTURE_DIR = os.path.join(BASE_DIR, "data/scenes")

    # --- 数据库配置 ---
    SQLITE_DB_PATH = os.path.join(BASE_DIR, "data/data.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + SQLITE_DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True

    # --- 日志配置 ---
    LOG_FILE = os.path.join(BASE_DIR, "app.log")

    DEBUG = True
