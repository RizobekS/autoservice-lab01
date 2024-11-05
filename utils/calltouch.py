import requests
from django.conf import settings
from django.http import HttpRequest


def send_calltouch_request(request: HttpRequest, subject: str, request_number: int = None, full_name: str = None,
                           phone_number: str = None, email: str = None, **extra_fields):
    assert full_name is not None or phone_number is not None or email is not None
    data = {
        'subject': subject or 'Не указано',
        'request_number': request_number,
        'fullName': full_name or 'Не указано',
        'phoneNumber': phone_number,
        'email': email,
        'requestUrl': request.build_absolute_uri(),
        **{f'customField[{name}]': value
           for name, value in extra_fields.items()}
    }

    # Send data to Calltouch
    response = requests.post(
        f'https://api.calltouch.ru/calls-service/RestAPI/requests/{settings.CALLTOUCH_SITE_ID}/register/',
        data=data
    )
    print(response.json())
    print(response.status_code)
