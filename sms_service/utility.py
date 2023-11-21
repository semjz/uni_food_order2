import http.client
import json
from django.conf import settings


def send_sms(message, recipient_number):
    conn = http.client.HTTPSConnection("api.sms.ir")
    print(message)
    payload = json.dumps({
        "lineNumber": settings.SMS_IR_NUMBER,
        "messageText": message,
        "mobiles": [
            recipient_number
        ],
        "sendDateTime": None
    })
    headers = {
        'X-API-KEY': settings.SMS_IR_X_API_KEY,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/send/bulk", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return data