import uuid
import requests
from requests.auth import HTTPBasicAuth

merchant_id = 523916
income_secret_key = 'DBaU3ZzmALNsExoD'
outcome_secret_key = 'AcxCrC2HKzXz92cV'
auth = HTTPBasicAuth(merchant_id, income_secret_key)
payment_url = "https://api.paybox.money/v4/payments"

def make_uuid():
    return str(uuid.uuid4())

def get_payment_details(id):
    return requests.get(f"{payment_url}/{id}", auth=auth)

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
        return r

