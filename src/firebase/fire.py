from typing import List

import firebase_admin
from firebase_admin import messaging, credentials

from my_secrets import FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY, FIREBASE_PRIVATE_KEY_ID, FIREBASE_PROJECT_ID, \
    FIREBASE_CLIENT_ID, FIREBASE_CERT
from src.parser.supabase import SupaBaseWorker

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": FIREBASE_PROJECT_ID,
    "private_key_id": FIREBASE_PRIVATE_KEY_ID,
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZ0oJQvZqA+8G9\naWVdbXhFMdL1BQWV+CzzHVn9ESPPYTce5sd/ZF4COF05oFG0HZsjQumtvZjwQAVH\nZXyfX0oUiwjA/b8EL3X+9iaGB9QLmjPX5AW38bt40exF9kaFfOst09iJrrUuae8Y\nO7nEjCTvg6R/vTp9XIHzveiyXZe7rvOGmp18ssV+W14aP6e7bDPWo7YMddNbxYTS\nMMeNOwzOX6pEZh2MYpiwTPjdSGOSoPHlO4VrKkihbmFNdab9NmaVkIC5TzqWKoxv\nCbKB620J4Hcll6MqMA0MyPdCwEy0VixoiOR+iMghFxpF6+xlTjRIpw6wAwqPqDbu\nEsNPr6d1AgMBAAECggEAA4WW1ztoGLDq8CfEGt4BRXBNGLALPzJF8TEIWOt2Cu76\nYJo/EhMdteZNeB7MEBgnb6i+CezP3hxRIp/XuRxo6Ux/oE+O+o0Nog9HtYTjXXqj\n2jsNyHbf6HXB954aYj8IcW2qxQg7fLsPLtpbN/1PcS5t60DNYIZoMUj1VXQgH7tq\nGutYc7h+jZma2Dwam1G49Eym2BNkFoBPj3X1ZsN6X/qypNMW7lntvOWFaG+cLbXF\nf4iHuOVgxbGz3nQ/81qwXIPSDXDkdimAwLK+XgrZB6BIBJKouOZM1hWab4/qO0UR\nRy94v9XJYa0L+X4OAPgz7Nb1jZFxoQncGsfkznRuwQKBgQDU9nXcrQ15+Fwi5cjS\nkCT9mKZfp95pSMhgxKrAgf26Nqr96LbZ1lYCwOapZ5a6zOZ7Hp0j0wVyDFGq8Sag\nNs/IKVaeNQH75nuhTIeXJFkDF2ubl98p8vTNPPeGs8AyWDEl5ovUSFOAUs0y0DSX\nb5YmXFF8+ZoDZy38zhjQyjb/FQKBgQC46HFLKhP5W9RVFGX4KDyAifppog5jAyOw\nKZXq8NDKid+7MocgqTEqkOxFvgeKsMB8LvEVWCXrIO5hinA58LAzPrpB19Ma2VFw\nWMNExl/8gV/ZGsjjEbGG4/XchsBUgaC1mHdm1EWfP+1SmJnRKN3cx8IYZ4D3Cdra\nY4nBquEe4QKBgQDG/xH9Rft8yJWXym4QS7809MoqQhty+B69RahkwFMOCP1Yy3bp\nMP4oDoa7L1/KZ6LK0z109z90ZYx+ll5IgU9BM1eL9+5FqwZFH9TnZ4CBggX8Wzqd\n4Tfc/CYzyY1DveMXDkoE8ByOoVC7NZCfHRcJ+2PtyvKeUXDIdPD9UKd5TQKBgB4u\nSnezSYlU9MZiSvaDUsTEQKxHOEPu+j9BumeboOi+Mldyut2Y4B6LgxUrHD4F9ZUP\ncGhEeAP13xLqrsC2SXxDy9D9ckaanBFTW6P5ISes0kE0fv+ZHrnesX2qPPBOLDYX\nyb1t/mMs4watQ8YA/p2PuV2UX1dzM1acEpsa0h3hAoGAfa0M6zbF0LcQsxatWj0u\nLOA//jk8/WgGifCbVGGqz1j+szIsY9U7+VKd3KGbL9FJTlar0zCOla0AZ1vpe32Q\n2UGSafAWOkGg+m5+HT2sLQFQdOsLWlWvErebcBqwHOJY99o2cmLdoXiQ+NIcofN/\n1EvWbwAd1wl3JxQdi6Ghydw=\n-----END PRIVATE KEY-----\n",
    "client_email": FIREBASE_CLIENT_EMAIL,
    "client_id": FIREBASE_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": FIREBASE_CERT,
    "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)


def send_single_message(title: str, body: str, token: str):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={'title': title, 'body': body},
        token=token
    )
    response = messaging.send(message)
    return response


def send_message_to_topic(title: str, body: str, sup: SupaBaseWorker):
    registration_tokens = sup.getSubs()

    web_subs = [sub.token for sub in registration_tokens if sub.clientID == 1]
    android_subs = [sub.token for sub in registration_tokens if sub.clientID == 2]
    if len(web_subs) > 0:
        message = messaging.MulticastMessage(
            data={'title': title, 'body': body},
            tokens=web_subs,
        )
        try:
            response = messaging.send_each_for_multicast(message)
            print('Successfully sent message web:', response)
        except Exception as e:
            print(e)
    if len(android_subs) > 0:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data={'title': title, 'body': body},
            tokens=android_subs,
        )
        try:
            response = messaging.send_each_for_multicast(message)
            print('Successfully sent message android:', response)
        except Exception as e:
            print(e)
