
from datetime import datetime, timezone
from pathlib import Path
import uuid

from bson import ObjectId
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from app.schemas.user import UserLogin
from app.database.mongodb import users_collection
from app.services.auth_service import (
    create_password_hash,
    check_password,
)
from app.security.jwt import (
    create_access_token,
    verify_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = HTTPBearer()

# Profile picture directory
BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads" / "profile_pictures"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024


# --------------------------------------------------
# AUTHENTICATION HELPER
# --------------------------------------------------

def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    token = credentials.credentials
    user_id = verify_access_token(token)

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in token"
        )

    user = users_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# --------------------------------------------------
# PROFILE PICTURE HELPER
# --------------------------------------------------

async def save_profile_picture(profile_picture: UploadFile):

    if profile_picture.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, and WEBP images are allowed"
        )

    image_data = await profile_picture.read()

    if not image_data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty"
        )

    if len(image_data) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Profile picture must be smaller than 5 MB"
        )

    extension = ALLOWED_IMAGE_TYPES[profile_picture.content_type]
    filename = f"{uuid.uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(image_data)

    return f"/uploads/profile_pictures/{filename}"


def delete_old_profile_picture(image_url):

    if not image_url:
        return

    filename = Path(image_url).name
    old_file = UPLOAD_DIR / filename

    if old_file.parent.resolve() == UPLOAD_DIR.resolve():
        if old_file.exists() and old_file.is_file():
            old_file.unlink()


# --------------------------------------------------
# REGISTER USER
# --------------------------------------------------

@router.post("/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_picture: UploadFile | None = File(None),
):

    name = name.strip()
    email = email.strip().lower()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required"
        )

    if len(password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters"
        )

    existing_user = users_collection.find_one(
        {"email": email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    profile_picture_url = None

    if profile_picture and profile_picture.filename:
        profile_picture_url = await save_profile_picture(
            profile_picture
        )

    new_user = {
        "name": name,
        "email": email,
        "password": create_password_hash(password),
        "profile_picture": profile_picture_url,
        "created_at": datetime.now(timezone.utc)
    }

    result = users_collection.insert_one(new_user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "profile_picture": profile_picture_url
    }


# --------------------------------------------------
# LOGIN USER
# --------------------------------------------------

@router.post("/login")
def login_user(user: UserLogin):

    email = user.email.strip().lower()

    existing_user = users_collection.find_one(
        {"email": email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not check_password(
        user.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token({
        "sub": str(existing_user["_id"])
    })

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# --------------------------------------------------
# GET CURRENT USER PROFILE
# --------------------------------------------------

@router.get("/me")
def get_current_user(
    user=Depends(get_authenticated_user)
):

    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "profile_picture": user.get("profile_picture")
    }


# --------------------------------------------------
# UPDATE PROFILE
# --------------------------------------------------

@router.put("/update-profile")
async def update_profile(
    name: str = Form(...),
    email: str = Form(...),
    profile_picture: UploadFile | None = File(None),
    user=Depends(get_authenticated_user)
):

    name = name.strip()
    email = email.strip().lower()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required"
        )

    # Prevent duplicate email addresses
    existing_email = users_collection.find_one({
        "email": email,
        "_id": {"$ne": user["_id"]}
    })

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    update_data = {
        "name": name,
        "email": email,
        "updated_at": datetime.now(timezone.utc)
    }

    new_picture_url = None

    if profile_picture and profile_picture.filename:

        new_picture_url = await save_profile_picture(
            profile_picture
        )

        update_data["profile_picture"] = new_picture_url

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": update_data}
    )

    if new_picture_url:
        delete_old_profile_picture(
            user.get("profile_picture")
        )

    updated_user = users_collection.find_one(
        {"_id": user["_id"]}
    )

    return {
        "success": True,
        "message": "Profile updated successfully",
        "user": {
            "id": str(updated_user["_id"]),
            "name": updated_user.get("name", ""),
            "email": updated_user.get("email", ""),
            "profile_picture": updated_user.get("profile_picture")
        }
    }


# --------------------------------------------------
# CHANGE PASSWORD
# --------------------------------------------------

@router.put("/change-password")
def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    user=Depends(get_authenticated_user)
):

    if not check_password(
        current_password,
        user["password"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    if len(new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="New password must contain at least 6 characters"
        )

    if current_password == new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )

    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "password": create_password_hash(new_password),
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return {
        "success": True,
        "message": "Password changed successfully"
    }
