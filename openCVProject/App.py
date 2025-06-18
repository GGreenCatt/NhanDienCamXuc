from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque
import pandas as pd
import datetime

app = Flask(__name__)

# Load mô hình đã huấn luyện
model = load_model("emotion_model.h5", compile=False)

# Load file nhận diện khuôn mặt từ OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Danh sách cảm xúc
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Bộ nhớ đệm để làm mịn cảm xúc
emotion_history = deque(maxlen=10)

# Biến toàn cục để lưu cảm xúc mới nhất
latest_emotion = "Neutral"

# Lưu lịch sử cảm xúc vào file CSV
emotion_log = []

# Khởi động camera
cap = cv2.VideoCapture(0)

def generate_frames():
    global latest_emotion
    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (64, 64))
            face = face.astype('float32') / 255.0
            face = np.expand_dims(face, axis=0)
            face = np.expand_dims(face, axis=-1)

            # Dự đoán cảm xúc
            preds = model.predict(face)
            predicted_emotion = emotion_labels[np.argmax(preds)]

            # Làm mượt cảm xúc
            emotion_history.append(predicted_emotion)
            most_common_emotion = max(set(emotion_history), key=emotion_history.count)

            # Cập nhật cảm xúc mới nhất
            latest_emotion = most_common_emotion

            # Lưu vào lịch sử
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emotion_log.append([timestamp, latest_emotion])

            # Vẽ khung + hiển thị cảm xúc
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, most_common_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Chuyển đổi frame sang định dạng JPEG để truyền về Web
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# API để gửi cảm xúc mới nhất đến giao diện
@app.route('/current_emotion')
def current_emotion():
    return jsonify({"emotion": latest_emotion})


if __name__ == "__main__":
    app.run(debug=True)
