import requests
import time
import json

from .api.auth import generate_signature
from .api.endpoint import CustomerApiEndpoint


class FivaldiPartnerClient:
    def __init__(self, partner_id, secret):
        self._partner_id = partner_id
        self._secret = secret

    @property
    def partner_id(self):
        return self._partner_id

    def generate_signature(self, http_method, epoch, endpoint, body, content_type):

        return generate_signature(
            partner_id=self._partner_id,
            partner_secret=self._secret,
            http_method=http_method,
            epoch=epoch,
            endpoint=endpoint,
            body=body,
            content_type=content_type
        )

    @property
    def api(self):
        return CustomerApiEndpoint(client=self)

    def ping(self):
        API_ENDPOINT = "/customer/api/customers"
        HTTP_METHOD = "GET"
        CONTENT_TYPE = "application/json"

        # body = open('body.json', 'r', encoding='utf8').read()
        # body = json.loads(body)
        # body = json.dumps(body)
        body = None

        # Get the current UNIX Epoch.
        epoch = str(int(time.time()))

        # Create the signature.
        signature = self.generate_signature(
            http_method=HTTP_METHOD,
            epoch=epoch,
            endpoint=API_ENDPOINT,
            body=body,
            content_type=CONTENT_TYPE
        )

        # Defining the headers that will be sent to the endpoint.
        HEADERS = {
            'Content-Type': CONTENT_TYPE,
            'X-Fivaldi-Partner': self.partner_id,
            'X-Fivaldi-Timestamp': epoch,
            'Authorization': signature,
        }

        if HTTP_METHOD == "GET":
            # Send the request.
            r = requests.get(url="https://api.fivaldi.net" + API_ENDPOINT, headers=HEADERS, timeout=360)
            print(str(r.status_code) + " " + str(r.reason) + " | " + str(r.text))
        elif HTTP_METHOD == "POST":
            # Send the request.
            r = requests.post(url="https://api.fivaldi.net" + API_ENDPOINT, headers=HEADERS, data=body, timeout=360)
            print(str(r.status_code) + " " + str(r.reason) + " | " + str(r.text))
        else:
            print("Invalid HTTP Method")
