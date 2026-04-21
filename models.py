from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Video(db.Model):
    __tablename__ = "videos"

    video_id = db.Column(db.String(10), primary_key=True)  # 10位数字，唯一主键
    file = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(500), default="")
    preview = db.Column(db.String(100), default="")
