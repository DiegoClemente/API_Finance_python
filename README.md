# PIX Payment API

This project is a Flask-based API for managing PIX payments, a Brazilian instant payment system. It provides endpoints for creating payments, generating QR codes, and handling payment confirmations.

## Features

- Create PIX payments
- Generate QR codes for payments
- Handle payment confirmations
- Real-time payment status updates using WebSockets

## Technologies Used

- Python 3.x
- Flask
- Flask-SocketIO
- Flask-SQLAlchemy
- SQLite
- Pillow (for image processing)
- QRCode (for generating QR codes)

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pix-payment-api.git
   cd pix-payment-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application:
   ```
   python app.py
   ```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

- `POST /payments/pix`: Create a new PIX payment
- `GET /payments/pix/qr_code/<file_name>`: Get the QR code image for a payment
- `POST /payments/pix/confirmation`: Confirm a PIX payment
- `GET /payments/pix/<payment_id>`: Get payment details and status

## WebSocket Events

- `connect`: Triggered when a client connects
- `disconnect`: Triggered when a client disconnects
- `payment_confirmed_<payment_id>`: Emitted when a payment is confirmed

## Project Structure

- `app.py`: Main application file
- `db_models/`: Database models
- `payments/`: Payment processing logic
- `repository/`: Database interaction
- `static/`: Static assets (CSS, images)
- `templates/`: HTML templates
- `tests/`: Unit tests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).