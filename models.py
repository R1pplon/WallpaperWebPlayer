from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Video(db.Model):
    __tablename__ = "videos"

    video_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(500), default="")
    preview = db.Column(db.String(100), default="")
    file = db.Column(db.String(255), nullable=False)

class Scene(db.Model):
    __tablename__ = "scenes"

    scene_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(500), default="")
    preview = db.Column(db.String(100), default="")
