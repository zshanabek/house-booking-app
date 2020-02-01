import requests
from rest_framework import status
import urllib3

class Payment:
    def __init__(self):
        self.merchant_id = 22403
        self.amount = 21
        self.order_id = 1
        self.description = "payment"
        self.url = "https://api.paybox.money/v4/payments"

    def _get_body(self):
        body = {
            "order": "my-super",
            "amount": 20,
            "refund_amount": 0,
            "currency": "KZT",
            "description": "Описание заказа",
            "payment_system": "TEST",
            "cleared": True,
            "expires_at": "Сутки",
            "language": "ru",
        }
        return body

    def initialize_payment(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        body = self._get_body()
        headers = {'Authorization': 'my-app/0.0.1'}
        r = requests.post(self.url, data=body, verify=False, headers=headers)
        print(r.text)
p = Payment()
p.initialize_payment()