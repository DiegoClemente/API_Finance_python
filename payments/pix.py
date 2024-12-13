import uuid
import qrcode

class Pix:
    def __init__(self):
        pass
    
    def create_payment(self, base_dir=""):
        # Implement logic to create a payment using PIX (Pay Internet Banking)
        bank_payment_id = str(uuid.uuid4())

        #qr_code
        hash_payment = f'hash_payment_{bank_payment_id}'
        qr = qrcode.make(hash_payment)
        qr.save(f'{base_dir}static/img/{bank_payment_id}.png')

        
        return {"bank_payment_id": bank_payment_id,
                "qr_code_path": f'{bank_payment_id}'}