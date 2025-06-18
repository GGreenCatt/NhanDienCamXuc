HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG NHẬN DIỆN CẢM XÚC AI

1. Giới thiệu
Ứng dụng Nhận diện Cảm xúc AI sử dụng Flask, OpenCV và TensorFlow/Keras để phân tích biểu cảm khuôn mặt theo thời gian thực. Hệ thống sẽ dự đoán cảm xúc và hiển thị kết quả trên giao diện web.

2. Cài đặt và chạy ứng dụng

2.1. Yêu cầu hệ thống
- Python 3.8 hoặc mới hơn
- Thư viện cần thiết: `Flask`, `OpenCV`, `TensorFlow`, `numpy`, `pandas`
- Webcam hoạt động

2.2. Cài đặt môi trường
Trước khi chạy ứng dụng truy cập vào cmd và mở folder C:\Users\hantr\openCVProject, cài đặt các thư viện cần thiết bằng lệnh:

pip install -r requirements.txt


2.3. Chạy ứng dụng
Chạy tập tin `App.py`:

```bash
python App.py
```

Sau khi chạy, Flask server sẽ khởi động trên **http://127.0.0.1:5000/**

Mở trình duyệt và truy cập vào đường dẫn trên để sử dụng ứng dụng.



3. Cách sử dụng
1. Khi truy cập vào giao diện web, hệ thống sẽ tự động kích hoạt webcam.
2. Mô hình sẽ nhận diện khuôn mặt và phân loại cảm xúc (Happy, Sad, Angry, Neutral, Surprise, Fear, Disgust).
3. Cảm xúc mới nhất sẽ được hiển thị trên màn hình.
4. Màu sắc viền video sẽ thay đổi theo cảm xúc:
   - 🟡 **Happy**: Vàng
   - 🔵 **Sad**: Xanh
   - 🔴 **Angry**: Đỏ
   - 🟣 **Surprise**: Tím
   - ⚫ **Neutral**: Xám
5. Emoji tương ứng với cảm xúc sẽ thay đổi theo thời gian thực.



4. Cấu trúc tệp
4.1. `App.py` (Backend)
- Khởi động Flask server.
- Sử dụng OpenCV để nhận diện khuôn mặt.
- Dự đoán cảm xúc bằng mô hình `fer_model.h5`.
- Trả về kết quả theo thời gian thực.

4.2. `fer_model.h5` (Mô hình AI)
- Mô hình nhận diện cảm xúc dựa trên CNN đã được huấn luyện trước.

4.3. `index.html` (Frontend)
- Giao diện web hiển thị video từ webcam.
- Cập nhật cảm xúc và hiệu ứng ánh sáng theo thời gian thực.



5. API Flask
| API Endpoint        | Phương thức | Chức năng |
|---------------------|------------|-----------|
| `/`                | `GET`       | Hiển thị giao diện web. |
| `/video_feed`      | `GET`       | Truyền video trực tiếp từ webcam. |
| `/current_emotion` | `GET`       | Lấy cảm xúc mới nhất dưới dạng JSON. |


6. Lưu ý
- Cần đảm bảo webcam hoạt động.
- Nếu camera không mở, kiểm tra quyền truy cập.
- Có thể tinh chỉnh mô hình để cải thiện độ chính xác.


