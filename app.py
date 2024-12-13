from flask import Flask, jsonify, render_template, request, send_file
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
from flask_socketio import SocketIO


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)
socketio = SocketIO(app)


@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()
    if 'value' not in data:
        return jsonify({"error": "Missing value field in request body"}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)
    payment = Payment(value=data['value'], expiration_date=expiration_date)
    
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    payment.bank_payment_id = data_payment_pix['bank_payment_id']
    payment.qr_code = data_payment_pix['qr_code_path']

    db.session.add(payment)
    db.session.commit()

    return jsonify({"message": "Payment has been created", 
                    "payment": payment.to_dict()}), 201


@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_payment_pix_qrcode(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')
    

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    data = request.get_json()

    if 'bank_payment_id' not in data and "value" not in data:
        return jsonify({"error": "Invalid data payment"}), 400
    
    # Simulate payment confirmation
    payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()
    
    if not payment or payment.paid:
        return jsonify({"error": "Payment not found"}), 404
    
    if data.get("value") != payment.value:
        return jsonify({"error": "Invalid data payment"}), 400
    
    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment_confirmed_{payment.id}')  

    return jsonify({"message": "Payment has been confirmed"})

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def get_payment_pix(payment_id):
    payment = Payment.query.get(payment_id)

    if not payment:
        return render_template('404.html')
    
    if payment.paid:
        return render_template('confirmed_payment.html',
                               payment_id=payment.id, 
                                value=payment.value,)
    
    return render_template('payment.html', 
                           payment_id=payment.id, 
                           value=payment.value, 
                           host="http://127.0.0.1:5000",
                           qr_code=payment.qr_code)

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)    