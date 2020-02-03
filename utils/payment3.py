import requests
from rest_framework import status
import urllib3
from requests.auth import HTTPBasicAuth
import hashlib
import collections
import dicttoxml

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Payment:
    def __init__(self):
        self.secret_key = "DBaU3ZzmALNsExoD"
        self.merchant_id = 523916
        self.order_id = 1
        self.description = "payment"
        self.url = "https://api.paybox.money/init_payment.php"

    def _get_body(self):
        body = {
            "pg_merchant_id": self.merchant_id,
            "pg_order_id": "123",
            "pg_amount": 25,
            "pg_description": "Eminem",
            "pg_salt": "some_random_string",
        }
        return body

    def create_signature(self):
        body = self._get_body()
        body = collections.OrderedDict(sorted(body.items()))
        lst = list(body.values())
        res = ["payment.php"] + lst + [self.secret_key] 
        res = [str(i) for i in res]
        res = ';'.join(res).encode('utf-8')
        hashed = hashlib.md5(res).hexdigest()
        return hashed

    def initialize_payment(self):
        signature = self.create_signature()
        body = self._get_body()
        body['pg_sig'] = signature
        xml = str(dicttoxml.dicttoxml(body))
        xml = xml.replace("root>", "request>")
        r = requests.post(self.url, data=xml)
        print(xml)
        print(r.status_code)
        print(r.text)
p = Payment()
p.initialize_payment()