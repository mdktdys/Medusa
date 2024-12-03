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
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHZJUov9l/vgf0\nHIzi6TJ4bpvdA1UsFUAmPv5+pNZTy+n3XYbqULoaMNJMBp1VAg4EXj1gdFtzB3iV\nxnNUpb3fVJG6uT1lghu42blmCFWa1Qc9+IsbuvWlK4sDTsFj4P+LB3HsxJJdkiLw\nC34acC5sVWteH5qdo+DAgdS2s+5xoNHGOMfXXsKsGMABoGBdvhUdBNrYBSq0QMFJ\n9W6cAnqwHt0VHBGPwfk3k7mk5lEU43mcUXhOLdkLz9ukGBHTx9BFzlqK4ha3+3io\nUZpFTBKyTkDkNj1+3sMzscNC9Mv+NYjhqfdpLusUVOtizrfRnrV5x52pjblQidp8\nlopD8gkPAgMBAAECggEAAMqDGNf3/iUQGv9v8orLgbEf1OJNmvEf5MS5qgzbwDLw\nxxA1hQBgw3S09wE+JejTa8IuSZDVhJGrSd+vIu5FcOnY5twX8Q5CrmZpYIHqBujN\nty/KeYfNh9P5Rmy4GCs8RjjjauqG/p34zshM49+LcE0UDk9KDMzBGLDlDRs5w6x4\njX+8V37t/w9yQbsKe0wmCPMON0E7nIGBaGmKYayZHwgoC9Z/6KvQyoRcrucSQAVe\nclzf2ha8B8VI01zZ0x5RgK9+pIGv1bYnL1+I2WwuC4+7BtKs28szyfIYiAOZfH6o\npPJg8cRlzQ5cEiqOORJe3i1l/t+6A6ejyOglUIG+WQKBgQD0UCncfwzHHEkR7wvY\n6qWhArbWeEwqczCZ75nuTOscOZaVFs3M3xBMmeo6rmIBEsdID+1RZeuRtpUXQIE4\nYEop95qzfXlZfGlvlBF92REoMd4JCo7+KV5qEgwoYtM2dr1HEHMV3WTHa1ImKQOY\ncDFfJR0WApwxrCjzzb+12cLt8wKBgQDQ7lR58QF24lZS9QprK+BOAFniJbipcKc4\n5Bh8uWdFLUNM+SdQbDLb1LMGVcQ4UCfsvNeBQEbexP2h7MyI0GfmSEnNu3v5jykc\nv8rfSKu73VadFdotVFzX4IM5D/+kLesTmtnw2ylDoKry8MehrZsdk2z/rJxbov1b\n/IkUAFTTdQKBgQDf3aS+Gt0GhfCeskBU344tX2NSWqDQNQTPyTFvnqPBFTPaIS8r\nDyrMRizO4IOFIEPi0FVRROb6eidbSwwdMH5EvlHPLqZHTSz/xNnSS1jhT/B4sGge\nlKGi6C6jwwpu2ZbOy0/pNRjncnuv490bjZJv8H4acQHWsj5ESL/mTkfD6QKBgGQM\nbMmD/laGph3Nl7KgbSYNBv3DYH1LI9ibaZp4UhqPRTYb7ZaWaXhZj20OLwtkXun/\nuBb9x7IvlOEwevVdDxP4M9df20szIdXRhf2MWCh7IlnQuAyS5G6/5TazEZD2KCbY\nNVsgJ89ppdL2ODKU5r2v9jcs2icLktW0xZOdYQFtAoGAV9ATg39wuYORsfQCswWH\n3XVVmHkVlpDXZ+XvP+89vZ+PIETgaG6ev1NInutBCO220ZkRwfCp/VBrZOAC29Ea\nDdZsvZBEatLMG2kI1mbE/jeRyOOm/DpLA9KfXw1TsURPyOrdPMqgtWxxG5HzTmNT\nHFHQIZNHm5AYNfp56JXoeJk=\n-----END PRIVATE KEY-----\n",
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
    print(FIREBASE_PROJECT_ID)
    print(FIREBASE_PRIVATE_KEY_ID)
    print(FIREBASE_CLIENT_EMAIL)
    print(FIREBASE_CLIENT_ID)
    print(FIREBASE_CERT)

    message = messaging.Message(
        data={'title': title, 'body': body},
        token=token
    )
    return messaging.send(message)


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
