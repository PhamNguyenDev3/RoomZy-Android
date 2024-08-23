# Ứng dụng Đặt Phòng Khách Sạn

<img src="https://github.com/PhamNguyenDev3/RoomZy-Android/blob/master/image/Home1.png" alt="Hotel Booking App" width="600"/>

Đây là một ứng dụng đặt phòng khách sạn trên nền tảng Android với backend sử dụng Flask Web API và firebase để lưu trữ dữ liệu. Ứng dụng cho phép người dùng duyệt, đặt phòng và quản lý các đặt phòng của mình một cách tiện lợi.

## Cấu trúc Dự án

-   **Thư mục `android-app/`:** Chứa mã nguồn của ứng dụng Android viết bằng Java.
-   **Thư mục `flask-api/`:** Chứa mã nguồn của Web API xử lý các nghiệp vụ backend.

```bash
├── RoomZy
│   ├── app
│   ├── gradle
│   └── build.gradle
└── flask-api
    ├── app.py
    ├── models.py
    ├── requirements.txt
    └── .env
```

## Tính năng

### Ứng dụng Android

-   **Đăng nhập và Đăng ký:** Cho phép người dùng đăng nhập và tạo tài khoản mới.
-   **Duyệt Phòng:** Xem danh sách phòng, chi tiết phòng và tiện nghi.
-   **Đặt Phòng:** Đặt phòng với các ngày cụ thể và quản lý các đặt phòng.
-   **Quản lý Đặt Phòng:** Xem, cập nhật và hủy đặt phòng.
-   **Thông Báo:** Nhận thông báo về trạng thái đặt phòng và nhắc nhở.n.
-   **Hệ thống Voucher:** Áp dụng voucher để nhận giảm giá khi đặt phòng.

### Flask Web API

-   **API RESTful:** Cung cấp các endpoint để quản lý người dùng, phòng, đặt phòng và voucher.
-   **Tích hợp Cơ Sở Dữ Liệu:** Sử dụng SQLite hoặc PostgreSQL để lưu trữ dữ liệu người dùng và đặt phòng.
-   **Xác thực:** Bảo mật các endpoint API bằng JWT.
-   **Bảng điều khiển Admin:** Giao diện web để quản lý phòng, đặt phòng và voucher.
-   **Xử lý Lỗi:** Xử lý các lỗi thông dụng với thông báo rõ ràng.

## Hình Ảnh Minh Họa

### Giao diện Đăng nhập

![Login Screen]()
<img src="https://github.com/PhamNguyenDev3/RoomZy-Android/blob/master/image/DangNhap.png" alt="Hotel Booking App" width="600"/>



### Giao diện Danh sách Phòng
<img src="https://github.com/PhamNguyenDev3/RoomZy-Android/blob/master/image/ChiTietPhong.png" alt="Hotel Booking App" width="600"/>


## Công Nghệ Sử Dụng

### Ứng dụng Android

-   **Ngôn ngữ:** Java
-   **Giao diện Người Dùng:** XML layouts, Material Design
-   **Kết nối Mạng:** Retrofit/Volley cho API
-   **Lưu trữ Dữ liệu:** Room Database/Shared Preferences
-   **Thông Báo:** Firebase Cloud Messaging
-   **Môi trường Phát triển:** Android Studio
-   **...**

### Flask Web API

-   **Framework:** Flask
-   **Cơ Sở Dữ Liệu:** SQLite/PostgreSQL
-   **Xác Thực:** Flask-JWT-Extended
-   **Tài liệu API:** Swagger/OpenAPI
-   **Triển khai:** Gunicorn, Nginx
-   **...**

## Hướng Dẫn Cài Đặt

### Ứng dụng Android

1. **Clone repository:**
    ```bash
    git clone https://github.com/PhamNguyenDev3/RoomZy-Android.git
    ```
2. **Mở dự án trong Android Studio.**
3. **Build và chạy ứng dụng trên thiết bị giả lập hoặc thiết bị thực.**
4. **Cấu hình URL API trong lớp `ApiClient`.**

### Flask Web API

**Để biết thêm chi tiết về cách cài đặt và sử dụng API Flask, vui lòng tham khảo file [README.md trong thư mục `hotel-booking-api`](flask-api/README.md).**

### Ứng dụng Android

1. **Mở ứng dụng và đăng ký hoặc đăng nhập.**
2. **Duyệt danh sách phòng và chọn phòng muốn đặt.**
3. **Chọn ngày đặt và xác nhận đặt phòng.**
4. **Quản lý đặt phòng từ mục hồ sơ cá nhân.**

### Flask Web API

1. **Sử dụng các endpoint API để quản lý phòng, người dùng, đặt phòng và voucher.**
2. **Truy cập bảng điều khiển admin để quản lý các hoạt động khách sạn.**

## Đóng Góp

-   Fork repository.
-   Tạo một nhánh mới cho tính năng hoặc sửa lỗi của bạn.
-   Commit thay đổi và push nhánh.
-   Tạo một pull request với mô tả chi tiết về thay đổi của bạn.

## Giấy Phép

Dự án này được cấp phép dưới giấy phép MIT - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## Liên Hệ

-   **Tác giả:** PhamNguyenDev3
-   **Email:** phamnguyendev03999@gmail.com
-   **GitHub:** [PhamNguyenDev3](https://github.com/PhamNguyenDev3)

---
