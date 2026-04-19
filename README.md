# 🎬 简易本地视频站

一个基于 **Flask** 的轻量级本地视频浏览网站，
用于在 **手机浏览器中观看 Wallpaper Engine 下载的壁纸视频文件**。

---

## ✨ 功能

* 自动扫描 Wallpaper Engine 下载目录下的 `.mp4` 文件
* 从 `project.json` 读取视频标题与封面
* 生成网页视频列表，可直接播放
* 一键更新索引
* 响应式界面，手机端友好显示

---

## 🏗️ 项目结构

```
.
├── app.py               # 主程序
├── video_index.json     # 自动生成的视频索引
└── templates/
    ├── index.html       # 视频列表页
    └── video.html       # 播放页面
```

---

## ⚙️ 使用方法

1. 安装依赖

   ```bash
   pip install flask
   ```

2. 修改 `app.py` 中的视频目录路径为你的 Wallpaper Engine 内容目录

   ```python
   VIDEO_DIR = "C:\\SteamLibrary\\steamapps\\workshop\\content\\431960"
   ```

3. 启动程序

   ```bash
   python app.py
   ```

4. 在手机或电脑浏览器访问

   ```
   http://localhost:5000
   ```

   即可在网页中浏览和播放壁纸视频。

---

## 🧠 特点

* 无数据库，自动索引视频
* 即开即用，适合局域网访问
* 界面简洁，手机端体验良好
* 方便将 Wallpaper 视频当作普通视频观看
