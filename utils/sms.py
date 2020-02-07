import requests
import random
from rest_framework import status


class SMS:
    def __init__(self, phone):
        self.login = 'akvproject'
        self.password = 'N9dBdbRrWGmcJjP'
        self.phone = phone
        self.url = "https://smsc.kz/sys/send.php"

    def generate_code(self):
        return str(random.randint(1, 9999)).zfill(4)

    def _get_body(self):
        body = {
            'login': self.login,
            'psw': self.password,
            'phones': self.phone,
        }
        return body

    def send_message(self, message):
        body = self._get_body()
        body['mes'] = message
        r = requests.post(
            self.url, data=body, verify=False
        )
        if r.status_code == status.HTTP_200_OK:
            return {'response': True, 'message': 'Код успешно был отправлен'}, status.HTTP_200_OK
        else:
            return {'response': False, 'error_message': r.content}, status.HTTP_500_INTERNAL_SERVER_ERROR
