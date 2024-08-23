# Hướng dẫn tạo môi trường để chạy API với Flask và Firebase

## Mô tả

Dự án này sử dụng Flask để tạo API và Firebase để quản lý cơ sở dữ liệu. API cho phép người dùng đặt phòng, hủy đặt phòng, xem lịch sử đặt phòng, cập nhật giao dịch và quản lý voucher.

## Yêu cầu hệ thống

-   Python 3.6 trở lên
-   pip (Python package installer)

## Các bước cài đặt

### 1. Clone dự án từ repository

```sh
git clone <repository-url>
cd <repository-directory>
```

### 2. Tạo môi trường ảo

Tạo môi trường ảo để quản lý các gói phụ thuộc một cách độc lập:

```sh
python -m venv venv
```

Kích hoạt môi trường ảo:

-   **Trên Windows:**
    ```sh
    .\venv\Scripts\activate
    ```
-   **Trên macOS/Linux:**
    ```sh
    source venv/bin/activate
    ```

### 3. Cài đặt các gói phụ thuộc

```sh
pip install -r requirements.txt
```

### 4. Cấu hình Firebase

Bạn cần có tệp khóa tài khoản dịch vụ của Firebase (serviceAccountKey.json). Đặt tệp này vào thư mục gốc của dự án.

Cập nhật URL cơ sở dữ liệu Firebase trong mã nguồn nếu cần:

```python
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://roomzy-cbeb4-default-rtdb.firebaseio.com'
})
```

### 5. Chạy ứng dụng Flask

```sh
python app.py
```

Ứng dụng sẽ chạy ở chế độ debug trên `http://127.0.0.1:5000/`.

## Cấu trúc dự án

-   `app.py`: File chính chứa mã nguồn của API.
-   `serviceAccountKey.json`: Khóa tài khoản dịch vụ Firebase.
-   `requirements.txt`: Danh sách các gói phụ thuộc.

## Các endpoint của API

### 1. Đặt phòng

-   **URL:** `/book-room`
-   **Method:** `POST`
-   **Request body:**
    ```json
    {
      "userId": "string",
      "roomId": "string",
      "checkInDate": "YYYY-MM-DD",
      "checkOutDate": "YYYY-MM-DD",
      "voucherId": "string",
      "totalPrice": float
    }
    ```
-   **Response:**
    ```json
    {
        "message": "Booking successful",
        "bookingId": "string"
    }
    ```

### 2. Hủy đặt phòng

-   **URL:** `/cancel-booking`
-   **Method:** `DELETE`
-   **Query parameters:**
    -   `bookingId`: ID của booking cần hủy.
-   **Response:**
    ```json
    {
        "message": "Booking canceled successfully"
    }
    ```

### 3. Xem lịch sử đặt phòng

-   **URL:** `/booking-history`
-   **Method:** `GET`
-   **Query parameters:**
    -   `userId`: ID của người dùng.
-   **Response:**
    ```json
    [
      {
        "bookingId": "string",
        "roomId": "string",
        "checkInDate": "YYYY-MM-DD",
        "checkOutDate": "YYYY-MM-DD",
        "voucherId": "string",
        "voucherDetails": {
          "discount": "string",
          "maxDiscountAmount": float,
          "description": "string"
        },
        "totalPrice": float,
        "finalPrice": float,
        "status": "string",
        "bookingCode": "string",
        "checkInCode": "string",
        "roomInfo": {
          "address": "string",
          "image": "string",
          "subImages": ["string"],
          "name": "string",
          "description": "string"
        }
      }
    ]
    ```

### 4. Cập nhật số lượng giao dịch của người dùng

-   **URL:** `/update-transaction`
-   **Method:** `POST`
-   **Request body:**
    ```json
    {
        "userId": "string"
    }
    ```
-   **Response:**
    ```json
    {
        "message": "Transaction updated successfully",
        "qualifiedVouchers": ["string"]
    }
    ```

### 5. Lấy danh sách voucher của người dùng

-   **URL:** `/user-vouchers`
-   **Method:** `GET`
-   **Query parameters:**
    -   `userId`: ID của người dùng.
-   **Response:**
    ```json
    {
      "vouchers": [
        {
          "voucherId": "string",
          "name": "string",
          "description": "string",
          "discount": "string",
          "maxDiscountAmount": float,
          "image": "string",
          "receivedDate": "YYYY-MM-DD",
          "status": "string"
        }
      ]
    }
    ```

## Lưu ý

-   Đảm bảo bạn đã cài đặt và cấu hình đúng Firebase để các API hoạt động bình thường.
-   Thường xuyên kiểm tra và cập nhật các gói phụ thuộc để bảo mật và hiệu năng tốt nhất.

Chúc bạn thành công!
