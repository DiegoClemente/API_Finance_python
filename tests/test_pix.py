import sys
sys.path.append('../')
import pytest
import os
from payments.pix import Pix


def test_pix_create_payment():
    pix = Pix()
    
    #create a payment
    payment = pix.create_payment(base_dir="../")
    
    
    #check if bank_payment_id and qr_code_path exists
    assert 'bank_payment_id' in payment
    assert 'qr_code_path' in payment
    
    #check if qr_code_path is a valid file
    qr_code_path = payment["qr_code_path"]
    assert os.path.isfile(f'../static/img/{qr_code_path}.png')