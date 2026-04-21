from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import CurrentUser, get_current_user

router = APIRouter()


@router.get("/me")
def me(current: CurrentUser = Depends(get_current_user)) -> dict:
    u = current.user
    return {
        "id": u.id,
        "firebase_uid": u.firebase_uid,
        "email": u.email,
        "display_name": u.display_name,
        "photo_url": u.photo_url,
        "role": current.role,
        "locale": u.locale,
    }
