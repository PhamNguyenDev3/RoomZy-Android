from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, db
from datetime import datetime, timedelta

app = Flask(__name__)



# Initialize Firebase

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://roomzy-cbeb4-default-rtdb.firebaseio.com'
})


# Helper function to check room availability
def is_room_available(room_id, check_in_date, check_out_date):
    ref = db.reference(f'RoomAvailability/{room_id}')
    bookings = ref.get()
    check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')

    while check_in_date < check_out_date:
        date_str = check_in_date.strftime('%Y-%m-%d')
        if bookings and date_str in bookings and bookings[date_str]['status'] == 'booked':
            return False
        check_in_date += timedelta(days=1)
    return True

# API endpoint to book a room
@app.route('/book-room', methods=['POST'])
def book_room():
    data = request.json
    user_id = data['userId']
    room_id = data['roomId']
    check_in_date = data['checkInDate']
    check_out_date = data['checkOutDate']
    voucher_id = data.get('voucherId')
    total_price = data['totalPrice']

    if not is_room_available(room_id, check_in_date, check_out_date):
        return jsonify({'error': 'Room is not available for the selected dates'}), 400

    booking_id = f'booking{int(datetime.now().timestamp())}'
    booking_code = f'BOOK{int(datetime.now().timestamp())}'
    check_in_code = f'CHKIN{int(datetime.now().timestamp())}'

    final_price = total_price
    voucher_details = None

    if voucher_id:
        voucher_ref = db.reference(f'Voucher/{voucher_id}')
        voucher = voucher_ref.get()
        if voucher:
            discount_percent = int(voucher['GiamGia'].replace('%', ''))
            max_discount = voucher['GiaToiDa']
            discount_amount = min(total_price * discount_percent / 100, max_discount)
            final_price -= discount_amount
            voucher_details = {
                'discount': voucher['GiamGia'],
                'maxDiscountAmount': voucher['GiaToiDa'],
                'description': voucher['MoTa']
            }

    booking_data = {
        'userId': user_id,
        'roomId': room_id,
        'checkInDate': check_in_date,
        'checkOutDate': check_out_date,
        'voucherId': voucher_id,
        'voucherDetails': voucher_details,
        'totalPrice': total_price,
        'finalPrice': final_price,
        'status': 'confirmed',
        'bookingCode': booking_code,
        'checkInCode': check_in_code
    }

    db.reference(f'Booking/{booking_id}').set(booking_data)

    # Update RoomAvailability
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    while check_in < check_out:
        date_str = check_in.strftime('%Y-%m-%d')
        db.reference(f'RoomAvailability/{room_id}/{date_str}').set({
            'status': 'booked',
            'bookingId': booking_id
        })
        check_in += timedelta(days=1)

    return jsonify({'message': 'Booking successful', 'bookingId': booking_id}), 200


# @app.route('/booking-history', methods=['GET'])
# def booking_history():
#     user_id = request.args.get('userId')
#     if not user_id:
#         return jsonify({'error': 'User ID is required'}), 400
#     user_bookings_ref = db.reference('Booking')
#     user_bookings = user_bookings_ref.get()

#     bookings_list = []
#     if user_bookings:
#         for booking_id, booking_data in user_bookings.items():
#             if booking_data.get('userId') == user_id:
#                 booking_info = {
#                     'bookingId': booking_id,
#                     'roomId': booking_data['roomId'],
#                     'checkInDate': booking_data['checkInDate'],
#                     'checkOutDate': booking_data['checkOutDate'],
#                     'voucherId': booking_data['voucherId'],
#                     'voucherDetails': booking_data.get('voucherDetails', {}),
#                     'totalPrice': booking_data['totalPrice'],
#                     'finalPrice': booking_data['finalPrice'],
#                     'status': booking_data['status'],
#                     'bookingCode': booking_data['bookingCode'],
#                     'checkInCode': booking_data['checkInCode']
#                 }
#                 bookings_list.append(booking_info)

#     return jsonify(bookings_list), 200

@app.route('/booking-history', methods=['GET'])
def booking_history():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Lấy thông tin từ bảng Booking
    user_bookings_ref = db.reference('Booking')
    user_bookings = user_bookings_ref.get()

    # Kiểm tra nếu không có booking
    if not user_bookings:
        return jsonify([]), 200

    # Lấy thông tin từ bảng Room
    rooms_ref = db.reference('Room')
    rooms = rooms_ref.get()

    bookings_list = []
    for booking_id, booking_data in user_bookings.items():
        if booking_data.get('userId') == user_id:
            room_id = booking_data.get('roomId')
            room_info = next((room for room in rooms.values() if room['Id'] == room_id), {})

            booking_info = {
                'bookingId': booking_id,
                'roomId': booking_data['roomId'],
                'checkInDate': booking_data['checkInDate'],
                'checkOutDate': booking_data['checkOutDate'],
                'voucherId': booking_data['voucherId'],
                'voucherDetails': booking_data.get('voucherDetails', {}),
                'totalPrice': booking_data['totalPrice'],
                'finalPrice': booking_data['finalPrice'],
                'status': booking_data['status'],
                'bookingCode': booking_data['bookingCode'],
                'checkInCode': booking_data['checkInCode'],
                'roomInfo': {
                    'address': room_info.get('Address', ''),
                    'image': room_info.get('Image', ''),
                    'subImages': room_info.get('SubImage', []),
                    'name': room_info.get('Name', ''),
                    'description': room_info.get('description', '')
                }
            }
            bookings_list.append(booking_info)

    return jsonify(bookings_list), 200

# API endpoint to cancel a booking
@app.route('/cancel-booking', methods=['DELETE'])
def cancel_booking():
    booking_id = request.args.get('bookingId')

    if not booking_id:
        return jsonify({'error': 'Missing booking_id parameter'}), 400

    db_ref = db.reference()
    booking_ref = db_ref.child('Booking').child(booking_id)
    booking_info = booking_ref.get()

    if not booking_info:
        return jsonify({'error': 'Booking not found'}), 404

    room_id = booking_info.get('roomId')
    check_in_date = booking_info.get('checkInDate')
    check_out_date = booking_info.get('checkOutDate')

    # Update RoomAvailability
    check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
    check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
    while check_in < check_out:
        date_str = check_in.strftime('%Y-%m-%d')
        db_ref.child(f'RoomAvailability/{room_id}/{date_str}').delete()
        check_in += timedelta(days=1)

    # Update voucher status if applicable
    user_id = booking_info.get('userId')
    voucher_id = booking_info.get('voucherId')
    if voucher_id:
        user_voucher_ref = db_ref.child('UserVoucher').child(user_id)
        vouchers = user_voucher_ref.child('vouchers').get()
        for voucher in vouchers:
            if voucher.get('voucherId') == voucher_id:
                voucher['status'] = 'unused'
                user_voucher_ref.update({'vouchers': vouchers})
                break

    # Delete booking information
    booking_ref.delete()

    return jsonify({'message': 'Booking canceled successfully'}), 200


# Endpoint to update user's transaction count
@app.route('/update-transaction', methods=['POST'])
def update_transaction():
    data = request.json
    user_id = data['userId']

    # Get the user's transaction count
    user_ref = db.reference(f'Users/{user_id}')
    user = user_ref.get()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    transactions_count = user.get('transactionsCount', 0) + 1
    user_ref.update({'transactionsCount': transactions_count})

    # Check if the user qualifies for a voucher
    vouchers_ref = db.reference('Voucher')
    vouchers = vouchers_ref.get()
    qualified_vouchers = []

    # Example condition: every 5 transactions earn a voucher
    if transactions_count % 5 == 0:
        for voucher_id, voucher in vouchers.items():
            qualified_vouchers.append(voucher_id)
            user_voucher_ref = db.reference(f'UserVoucher/{user_id}')
            user_vouchers = user_voucher_ref.child('vouchers').get() or []
            user_vouchers.append({
                'voucherId': voucher_id,
                'receivedDate': datetime.now().strftime('%Y-%m-%d'),
                'status': 'unused'
            })
            user_voucher_ref.update({'vouchers': user_vouchers})

    return jsonify({
        'message': 'Transaction updated successfully',
        'qualifiedVouchers': qualified_vouchers
    }), 200


@app.route('/user-vouchers', methods=['GET'])
def user_vouchers():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Get the user's vouchers
    user_voucher_ref = db.reference(f'UserVoucher/{user_id}/vouchers')
    user_vouchers = user_voucher_ref.get()
    print(user_vouchers)
    if not user_vouchers:
        return jsonify({'vouchers': []}), 200

    # Get detailed information for each voucher
    voucher_details = []
    for user_voucher in user_vouchers:
        voucher_id = user_voucher.get('voucherId')
        if not voucher_id:
            continue
        voucher_ref = db.reference(f'Voucher/{voucher_id}')
        voucher = voucher_ref.get()
        if voucher:
            voucher_details.append({
                'voucherId': voucher_id,
                'name': voucher.get('TenVC'),
                'description': voucher.get('MoTa'),
                'discount': voucher.get('GiamGia'),
                'maxDiscountAmount': voucher.get('GiaToiDa'),
                'image': voucher.get('Hinh'),
                'receivedDate': user_voucher.get('receivedDate'),
                'status': user_voucher.get('status')
            })

    return jsonify({'vouchers': voucher_details}), 200


@app.route('/check-connection', methods=['GET'])
def check_connection():
    try:
        db.reference('RoomAvailability').get()
        return jsonify({'message': 'Connection successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
