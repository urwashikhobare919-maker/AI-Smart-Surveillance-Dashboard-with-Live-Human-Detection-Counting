# AI Smart Surveillance Dashboard with Live Human Detection & Counting

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-WebApp-black)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

---

# 📌 Project Overview

The **AI Smart Surveillance Dashboard** is an advanced real-time human detection and people counting system developed using **Python, Flask, YOLOv8, OpenCV, SQLite, HTML, CSS, and JavaScript**.

This project uses Artificial Intelligence to detect people from live CCTV/webcam feed, count **IN / OUT movement**, monitor crowd level, generate alerts, and display everything on a modern web dashboard.

It is specially designed for:

- Smart Offices
- Colleges & Universities
- Malls
- Railway Stations
- Airports
- Shops
- Factories
- Smart Cities
- Security Systems

---

# 🚀 Key Features

## 🎯 AI Human Detection
- Detects humans in real-time using YOLOv8 model.
- Highly accurate detection.
- Works on webcam / CCTV camera.

## 👥 Live People Counting
- Counts people currently visible in frame.
- Tracks moving people.

## 🔼 IN / OUT Entry Counter
- Detects movement crossing virtual line.
- Counts people entering.
- Counts people exiting.

## 🚨 Crowd Alert System
- Automatically alerts when crowd exceeds limit.

## 📊 Live Dashboard
- Premium web dashboard UI.
- Real-time analytics.
- Camera monitoring page.
- Alerts page.
- Reports page.
- Settings page.

## 🗃 Database Logging
- Stores people count logs in SQLite database.

## 📈 Analytics
- Graphs for people movement.
- Entry/Exit history.

---

# 🛠 Technologies Used

| Technology | Purpose |
|----------|---------|
| Python | Backend Logic |
| Flask | Web Framework |
| YOLOv8 | AI Human Detection |
| OpenCV | Camera Processing |
| SQLite | Database |
| HTML/CSS | Frontend UI |
| JavaScript | Live Data Update |

---

# 📁 Project Structure

```bash
AI-Surveillance-System/
│── app.py
│── main.py
│── server.py
│── tracker.py
│── database.py
│── dashboard.py
│── camera_state.py
│── yolov8n.pt
│── people.db
│── data.db
│── templates/
│    │── index.html
│    │── camera.html
│    │── analytics.html
│    │── alerts.html
│    │── reports.html
│    │── settings.html
│── static/
│    │── style.css
│    │── script.js