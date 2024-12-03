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
    "private_key": FIREBASE_PRIVATE_KEY,
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
        data={'title': title, 'body': body},
        token=token
    )
    messaging.send(message)


def send_message_to_topic(title: str, body: str, sup: SupaBaseWorker):
    registration_tokens = sup.getSubs()

    web_subs = [sub.token for sub in registration_tokens if sub.clientID == 1]
    android_subs = [sub.token for sub in registration_tokens if sub.clientID == 2]
    if len(web_subs) > 0:
        message = messaging.MulticastMessage(
            data={'title': title, 'body': body},
            tokens=web_subs,
        )
        response = messaging.send_each_for_multicast(message)
        print('Successfully sent message web:', response)
    if len(android_subs) > 0:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data={'title': title, 'body': body},
            tokens=android_subs,
        )
        response = messaging.send_each_for_multicast(message)
        print('Successfully sent message android:', response)
