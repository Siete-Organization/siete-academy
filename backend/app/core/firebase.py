import json
import logging
from functools import lru_cache

import firebase_admin
from firebase_admin import auth, credentials

from app.core.config import get_settings

log = logging.getLogger(__name__)


@lru_cache
def _init_firebase() -> firebase_admin.App:
    settings = get_settings()
    if firebase_admin._apps:
        return firebase_admin.get_app()

    if settings.firebase_credentials_json:
        cred = credentials.Certificate(json.loads(settings.firebase_credentials_json))
    elif settings.firebase_credentials_path:
        cred = credentials.Certificate(settings.firebase_credentials_path)
    else:
        log.warning("No Firebase credentials configured; auth will fail until configured.")
        return firebase_admin.initialize_app()

    return firebase_admin.initialize_app(cred)


def verify_id_token(token: str) -> dict:
    _init_firebase()
    return auth.verify_id_token(token)


def set_custom_role(uid: str, role: str) -> None:
    _init_firebase()
    auth.set_custom_user_claims(uid, {"role": role})


def get_user(uid: str):
    _init_firebase()
    return auth.get_user(uid)
