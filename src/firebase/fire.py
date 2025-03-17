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
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCjC1MohR65YYXv\n4mxR23DfmmjiQq3/iHfVsAcy4w1QV1nX+zjQxvSdZh2JORi2z2oB5kLrSOxA2jrd\nZ8cVoJqUPyQPuP71ak0xHLFl5CELgU4sgYbFxTlrszaEzgzD42qjhaDhtJ45/dVj\nrjaDBvfplZPDdi1r9rNoEI/JNO7IbO/BFCzzbYUi5o3nNmubb+YPnNgySlck4MZU\njRBn2RDkMSAM6UtUdgtiYQ6nUj+9trHwKHrFyhcUMsX1vSFQQlbviPoTchHrgVvh\nRv8vvqKIO3vHFZ4BbVHO829hIbmcmPTcqyYibE2dmTa0Xw30fhcndS4VVODf9rdV\n2gqb3MrvAgMBAAECggEANB9Ps1lzLAJgRgLVbAnB+MmtFAALDfC7loWSl5L8U53J\nLAG09RFVa+gUMyUcoHyIQBkzdXI3jLf3L4aYn3JbWF8jER+r6hrUmIm6sH8QjVQG\nALZbtmfJZoPBPw18CTdvhN0YRG9wUcuy5w3vgU29/V+DAG6MMMKKMg9xV/pjB5FB\nGV2vn9XYDcu3Zd/AR8qvJFMDf0kdnZ/IzWgwtnXo4sTP+nznKQACLMxWgcmkz6jk\nAgBekq/RyQ8WEA1EfNOt9Olm5KBxjKdV/UWZQdDOBPnqbCK/becUXhIAGlXXDHlu\n1OIItqIOcsQDCVbX6P8C4JFcEGdGgO/dfZpm4WKfaQKBgQDSdQrzhwpOdCqgK0bs\nSgCNytNdYjxkeoL+89/ocsujOTldPwQ5p9Gk4YlBErt7PWf2FSoUi5p8iNxSP0oX\nYeSGJRyxdXOygHTD3W8JAftKN3cnhQGMH/75uYKoXUqp8DpTgZt4YvANjNFDHpVc\nYtNfenM2Exv7yne9clv5vkuPuwKBgQDGU7AP/qGB4fJZgrZSo4wGCOl+4+QAV3rk\nNk0Qg2VjfkyD0u4zb8cAn61sguG8aJT4/QTeTXZ0sPxopx9q7J366iB6vTWDzhwk\nBmPjE07maauFDEOO4pXrBweko44fE97tCUf9HUf21t6h4nnHRZrJFK7StP59PpJc\nyI0HOjF8XQKBgA53fzY4TSwRbjCuaOSrPZiBnb/oldAuX7zY1MZsxbTFpTzUrRyt\nfYrA+idf+0VAdloDIG5jHk57NfHtadFrqELUYEGOmlJl5CDmotBSs4xpfaZYzT9t\nn6BY8TNTnmNKIShGW4KOAoRb7rKXcpr0LCV/DFZmP+EyDMMYDlx/iUArAoGBAIW6\n4oo2eXMaBw+iWwxoKT/cfI3KXvB4DG6byuUqpJAtFq0A6wuWAIsEIK19p3ci0ej+\nu2ymsQxIVzq+DipMOM57VsFMmiwxK7qC8JGqcFZfxH8nYNqVIN/k0puKiYedH4GX\n84nSV7cy9dYU32amIZQbNTLxRnTvX0PfG3FXJQ0lAoGAUywSyAmcMw7ZCyvIMAy9\nU6h0BZlY4462mzgGRcUwQ+GvTVpWX1C6Lg1e9HSUPIZc2CmuixxkmskzIeS6Olz5\nK72vR9rDzRS8cgIdTp8/08ZnZDaL3qYtPlBmEXtIzcNwUaHEdwDo2ibRLuawtJck\nqzNuahgUmM+tPB3g+3Tus8U=\n-----END PRIVATE KEY-----\n",
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
            print('Successfully sent message web:', response.responses)
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
