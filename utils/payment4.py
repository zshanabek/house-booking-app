import uuid
import requests
from requests.auth import HTTPBasicAuth
import config

merchant_id = config.merchant_id
income_secret_key = config.income_secret_key
auth = HTTPBasicAuth(merchant_id, income_secret_key)
payment_url = "https://api.paybox.money/v4/payments"

def make_uuid():
    return str(uuid.uuid4())

class Payment:
    def __init__(self, amount, currency, description, order):
        self.currency = currency
        self.order = order
        self.amount = amount
        self.description = description

    def get_body(self):
        body = {
            "currency": "KZT",
            "order": self.order,
            "amount": self.amount,
            "description": self.description,
        }
        return body

    def create_payment(self):
        body = self.get_body()
        headers = {'X-Idempotency-Key': make_uuid()}
        r = requests.post(payment_url, json=body, auth=auth, headers=headers)
        return r.json()

    def get_payment(self, id):
        r = requests.get(f"{payment_url}/{id}", auth=auth)
        return r.json()

p = Payment(2000000, "KZT", "Good description", '243254345246')
# result = p.create_payment()
# print(result)
ok = p.get_payment(142972050)
print(ok)