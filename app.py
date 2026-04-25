from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
import threading
import time

app = Flask(__name__)

# ======================================
# LOAD MODEL
# ======================================
model = YOLO("yolov8n.pt")

# ======================================
# CAMERA OPEN (FINAL FIX)
# ======================================
def start_camera():
    # Try camera indexes 0,1,2
    for idx in [0, 1, 2]:
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            print("Camera Started :", idx)
            return cap

    # fallback
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        return cap

    return None


cap = start_camera()

# ======================================
# GLOBAL DATA
# ======================================
live_people = 0
in_count = 0
out_count = 0
alerts = 0

LINE_Y = 320

history = {}
counted = set()

frame_data = None
lock = threading.Lock()

# ======================================
# DETECTION THREAD
# ======================================
def detect_people():
    global cap, frame_data
    global live_people, in_count, out_count, alerts

    while True:

        if cap is None or not cap.isOpened():
            cap = start_camera()
            time.sleep(1)
            continue

        success, frame = cap.read()

        if not success:
            cap.release()
            cap = start_camera()
            time.sleep(1)
            continue

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1000, 600))

        try:
            results = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                classes=[0],
                conf=0.45,
                verbose=False
            )
        except:
            results = []

        live_people = 0

        if results and len(results) > 0:
            r = results[0]

            if r.boxes.id is not None:

                boxes = r.boxes.xyxy.cpu().numpy()
                ids = r.boxes.id.cpu().numpy().astype(int)

                live_people = len(ids)

                for box, pid in zip(boxes, ids):

                    x1, y1, x2, y2 = map(int, box)

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)

                    cv2.putText(frame, f'ID {pid}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                    # IN / OUT COUNT
                    if pid in history:

                        old_y = history[pid]

                        # IN
                        if old_y < LINE_Y and cy >= LINE_Y:
                            if (pid, "in") not in counted:
                                in_count += 1
                                counted.add((pid, "in"))

                        # OUT
                        elif old_y > LINE_Y and cy <= LINE_Y:
                            if (pid, "out") not in counted:
                                out_count += 1
                                counted.add((pid, "out"))

                    history[pid] = cy

        alerts = 1 if live_people >= 5 else 0

        # DRAW HUD
        cv2.line(frame, (0, LINE_Y), (1000, LINE_Y), (255,0,0), 3)

        cv2.putText(frame, f'LIVE PEOPLE : {live_people}', (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

        cv2.putText(frame, f'IN : {in_count}', (20,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.putText(frame, f'OUT : {out_count}', (20,120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.putText(frame, f'ALERTS : {alerts}', (20,160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,165,255), 2)

        with lock:
            frame_data = frame.copy()

# ======================================
# VIDEO STREAM (MAIN FIX)
# ======================================
def generate_frames():
    global frame_data

    while True:

        with lock:
            if frame_data is None:
                blank = 255 * 0 + 0
                img = cv2.imread("none.jpg")

                if img is None:
                    img = cv2.UMat(600, 1000, cv2.CV_8UC3).get()
                    img[:] = (0, 0, 0)

                cv2.putText(img, "Starting Camera...", (320, 300),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

                ret, buffer = cv2.imencode(".jpg", img)
            else:
                ret, buffer = cv2.imencode(".jpg", frame_data)

        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   buffer.tobytes() + b'\r\n')

        time.sleep(0.03)

# ======================================
# ROUTES
# ======================================
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/camera')
def camera():
    return render_template("camera.html")

@app.route('/analytics')
def analytics():
    return render_template("analytics.html")

@app.route('/alerts')
def alerts_page():
    return render_template("alerts.html")

@app.route('/reports')
def reports():
    return render_template("reports.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    return jsonify({
        "total": live_people,
        "in": in_count,
        "out": out_count,
        "alerts": alerts
    })

# ======================================
# START
# ======================================
if __name__ == "__main__":
    t = threading.Thread(target=detect_people)
    t.daemon = True
    t.start()

    app.run(debug=True, threaded=True, use_reloader=False)