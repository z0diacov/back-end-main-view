#fastapi
from fastapi import APIRouter, HTTPException, status, Request, BackgroundTasks, Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
#security
from security.jwt import jwt_handler
from security.hash import verify_password, hash_password
from security.config import GOOGLE_ADD_PASSWORD_TOKEN_EXPIRE_SECONDS
from schemas.jwt import JWTVerifyEmail, JWTResetPassword, JWTAccess, JWTRefresh, JWTGooglePassword
from security.otp import otp_client
#schemas
from schemas.profile_and_settings import HasPasswordResponse, CurrentUserProfileResponse, CurrentUserTrainerProfileResponse, UserProfileResponse, TrainerProfileResponse
from schemas.authentication import UserDataFromToken, OTPData
from schemas.profile_and_settings import ChangePassword, UsernameOnly, NameOnly, GoogleAddPassword, TrainerBioOnly
from schemas.authorization import EmailOnly

from database import mysql_client, redis_client
#datetime
from datetime import timedelta
#documentation
from documentation.profile_and_settings_responses import RESPONSES
#other
from typing import Annotated, Union
from security.authentication import auth_dependences
from service import mailer

router = APIRouter()

@router.put("/username",
    status_code=status.HTTP_200_OK, 
    summary="Username changing",
    responses=RESPONSES["PUT"]["/username"]
)
async def change_username(otp: OTPData, data: UsernameOnly, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication.
    2. Validation username, check existance in database. Already exist -> 409.
    3. Changing username in the database.
    """
    new_username = data.username
    user_id = user_data.uid
    otp = otp.otp

    async with mysql_client.cursor() as cursor:
        existing_user = await cursor.pull("SELECT * FROM users WHERE username = %s", (new_username,))
        
        if existing_user:
            raise HTTPException(status_code=409, 
                                detail="New username already exists")
        
        if not await otp_client.verify_otp(user_id, otp):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail="OTP expired or invalid")

        await cursor.push("UPDATE users SET username = %s WHERE id = %s", (new_username, user_id,))

    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})
    
@router.put("/password",
    status_code=status.HTTP_200_OK, 
    summary="Password changing",
    responses=RESPONSES["PUT"]["/password"]
)
async def change_password(data: ChangePassword, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Validation password, mathing hashed old password with password in the database. Not match -> 400.
    2. Authentication.
    3. Changing old password in the database to hashed new.
    """

    new_password = data.new_password
    old_password = data.old_password
    user_id = user_data.uid

    async with mysql_client.cursor() as cursor:
        user_record = await cursor.pull("SELECT * FROM users WHERE id = %s", (user_id,))
    
    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    
    current_hashed_password = user_record[0]["password"]

    if not verify_password(current_hashed_password, old_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect old password")
    
    if verify_password(current_hashed_password, new_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="New password must be different from the old one")
    
    hashed_new_password = hash_password(new_password)
    
    async with mysql_client.cursor() as cursor:
        await cursor.push("UPDATE users SET password = %s WHERE id = %s", (hashed_new_password, user_id))

    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.put("/name",
    status_code=status.HTTP_200_OK, 
    summary="Name changing",
    responses=RESPONSES["PUT"]["/name"]
)
async def change_name(data: NameOnly, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Validation name, if name mathes the old one -> 409
    2. Authentication.
    3. Changing old name in the database to new name.
    """ 

    new_name = data.name
    async with mysql_client.cursor() as cursor:
        old_name = await cursor.pull("SELECT name FROM users WHERE id = %s", (user_data.uid,))

    if new_name == old_name[0]["name"]:    
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="New name must be different from the old one")
    
    async with mysql_client.cursor() as cursor:
        await cursor.push("UPDATE users SET name = %s WHERE id = %s", (new_name, user_data.uid,))
    
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.put("/email",
    status_code=status.HTTP_200_OK, 
    summary="Email changing",
    responses=RESPONSES["PUT"]["/email"]
)
async def change_email(otp: OTPData, data: EmailOnly, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication.
    2. Validation email, check existance in database. Already exist -> 409.
    3. Verify OTP
    4. Changing email in the database.
    """
    ...

@router.post("/google/password/send",
    status_code=status.HTTP_200_OK, 
    summary="Create a link to create a password after registration with Google",
    responses=RESPONSES["POST"]["/google/password/send"]
)
async def send_google_password(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication.
    2. Check if user already has a password -> 409.
    3. Creating token with type `google_add_password` and `family` 1.
    4. Send email with link http://localhost:3000/google/password/add?token={token}
    5. Return 200 success.
    Notes:
    - Token will not be expired after first use, but password will exist -> after first use user will get 409.
    """
    user_id = user_data.uid

    async with mysql_client.cursor() as cursor:
        pull_by_uid = await cursor.pull("SELECT * FROM users WHERE id = %s", (user_id,))

    if pull_by_uid[0]["password"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="Password already exists")
    
    token = jwt_handler.create_token(
        data={
            "email": pull_by_uid[0]["email"],
            "family": 1
        },
        expired_seconds=GOOGLE_ADD_PASSWORD_TOKEN_EXPIRE_SECONDS,
        model=JWTGooglePassword,
    )

    add_password_url = f"http://localhost:3000/google/password/add?token={token}"
    print(f"{add_password_url=}")

    await mailer.send_email(
        message_type=JWTGooglePassword.model_fields["type"].default,
        recipient=pull_by_uid[0]["email"],
        data={'button_link': add_password_url}
    )

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"detail": "Success"})


@router.post("/google/password",
    status_code=status.HTTP_201_CREATED, 
    summary="Create a password after registration with Google",
    responses=RESPONSES["POST"]["/google/password"]
)
async def create_google_password(data: GoogleAddPassword, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Validation new password.
    2. Authentication.
    3. Validation the google add password token:
    - If invalid or expired, return 401.
    4. If user_id in the token does not match the user_id in the database -> 409.
    5. If password in the database is not null -> 409.
    6. Insert hashed password into the database.
    7. Return 201 success.
    """
    payload = jwt_handler.decode_token(data.token, JWTGooglePassword)

    user_id = user_data.uid
    email = payload.email
    new_password = data.new_password

    async with mysql_client.cursor() as cursor:
        pull_by_email = await cursor.pull("SELECT * FROM users WHERE email = %s", (email,))

    if pull_by_email[0]["id"] != user_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Token does not belong to current user")

    if pull_by_email[0]["password"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Password already exists")
    
    async with mysql_client.cursor() as cursor:
        hashed_password = hash_password(new_password)
        await cursor.push("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id,))
    
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"detail": "Success"})

@router.get("/me/has-password",
    status_code=status.HTTP_200_OK,          
    response_model=HasPasswordResponse,
    summary="Returned password existing", 
    responses=RESPONSES["GET"]["/me/has-password"]
)
async def has_password(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication.
    2. Return password existing in the database
    """ 
    user_id = user_data.uid
    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT password FROM users WHERE id = %s", (user_id),)
    
    password_exists = bool(user[0]["password"])

    return JSONResponse(status_code=status.HTTP_200_OK, 
                            content={"has_password": password_exists})


@router.get("/user/me/profile",
    status_code=status.HTTP_200_OK,          
    response_model=CurrentUserProfileResponse,
    summary="Returned current user profile",
    responses=RESPONSES["GET"]["/user/me/profile"]
)
async def get_current_user_profile(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authenticate the user.
    2. Return the current user profile, including:
       - username
       - email
       - name
       - profile_picture
       - is_trainer
       - registration_date
    """
    
    user_id = user_data.uid

    async with mysql_client.cursor() as cursor:
        user_record = await cursor.pull("SELECT username, email, name, created_at FROM users WHERE id = %s", (user_id,))

    user = user_record[0]

    async with mysql_client.cursor() as cursor:
        trainer_record = await cursor.pull("SELECT 1 FROM trainer_profiles WHERE user_id = %s", (user_id,))

    is_trainer = bool(trainer_record)

    return CurrentUserProfileResponse(
        username=user["username"],
        email=user["email"],
        name=user["name"],
        profile_picture_url=f"https://example.com/media/profile_pics/{user['username']}.jpg",
        is_trainer=is_trainer,
        registration_date=user["created_at"].isoformat(),
    )



@router.get("/trainer/me/profile",
    status_code=status.HTTP_200_OK,          
    response_model=CurrentUserTrainerProfileResponse,
    summary="Returned current user trainer profile", 
    responses=RESPONSES["GET"]["/trainer/me/profile"]
)
async def get_current_user_trainer_profile(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authenticate the user.
    2. Return the current user profile, including:
        - trainer_bio
        - balance
        - my_exercises
        - my_workouts
        - my_programs
    """
    async with mysql_client.cursor() as cursor:
        trainer = await cursor.pull("SELECT * FROM trainer_profiles WHERE id = %s", (user_data.uid,))
    
    if not trainer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="User is not a trainer")
    
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={
            "trainer_bio": trainer[0]["bio"],
            "balance": trainer[0]["balance"],
        }
    )

@router.get("/user/profile",
    status_code=status.HTTP_200_OK,          
    response_model=UserProfileResponse,
    summary="Returned user profile", 
    responses=RESPONSES["GET"]["/user/profile"]
)
async def get_user_profile(user_id: int):
    """
    Steps:
    1. Validate if the user with given `user_id` exists.
        - If not found, return 404 Not Found with appropriate message.

    2. If user exists, return their profile containing:
        - username
        - name
        - profile_picture
        - is_trainer (bool indicating trainer status)
        - registration_date
    """ 
    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT username, name, created_at FROM users WHERE id = %s", (user_id,))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User does not exist")
    
    async with mysql_client.cursor() as cursor:
        trainer = await cursor.pull("SELECT * FROM trainer_profiles WHERE user_id = %s", (user_id,))

    return UserProfileResponse(
        username=user[0]["username"],
        name=user[0]["name"],
        profile_picture_url=f"https://example.com/media/profile_pics/{user[0]["username"]}.jpg",
        is_trainer=bool(trainer),
        registration_date=user[0]["created_at"].isoformat()
    )


@router.get("/trainer/profile",
    status_code=status.HTTP_200_OK,          
    response_model=TrainerProfileResponse,
    summary="Returned trainer profile", 
    responses=RESPONSES["GET"]["/trainer/profile"]
)
async def get_trainer_profile(user_id: int):
    """
    Steps:
    1. Check if user_id exists
        - If not exists, return 404
    2. Check if exists trainer profile for that user
        - If not exists, return 404
    3. Return the user profile, including:
        - trainer_bio
        - trainer_exercises
        - trainer_workouts
        - trainer_programs
    """

    async with mysql_client.cursor() as cursor:
        user_record = await cursor.pull("SELECT id, username, email, name, created_at FROM users WHERE id = %s", (user_id,))
    
    if not user_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    async with mysql_client.cursor() as cursor:
        trainer_record = await cursor.pull("SELECT bio, balance FROM trainer_profiles WHERE user_id = %s", (user_id,))
    
    if not trainer_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trainer profile not found")

    trainer_bio = trainer_record[0]["bio"]

    async with mysql_client.cursor() as cursor:
        trainer_exercises = await cursor.pull("SELECT * FROM exercises WHERE author_user_id = %s", (user_id,))
        trainer_workouts = await cursor.pull("SELECT * FROM workouts WHERE author_user_id = %s", (user_id,))
        trainer_programs = await cursor.pull("SELECT * FROM programs WHERE author_user_id = %s", (user_id,))

    return TrainerProfileResponse(
        trainer_bio=trainer_bio,
        trainer_exercises=trainer_exercises,
        trainer_workouts=trainer_workouts,
        trainer_programs=trainer_programs
    )



@router.put("/trainer-bio",
    status_code=status.HTTP_200_OK, 
    summary="Trainer bio changing",
    responses=RESPONSES["PUT"]["/trainer-bio"]
)
async def change_name(data: TrainerBioOnly, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Validation trainer bio
    2. Authentication.
    3. If trainer bio matches the old one -> 409
    4. If user does not have trainer profile -> 403
    5. Changing old trainer bio in the database to new one.
    6. Return 200 success.
    """ 
    new_bio = data.trainer_bio

    async with mysql_client.cursor() as cursor:
        old_bio = await cursor.pull("SELECT bio FROM trainer_profiles WHERE id = %s", (user_data.uid,))

    if not old_bio:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You must create a trainer profile before updating your bio")
    
    if new_bio == old_bio[0]["bio"]:    
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="New trainer_bio must be different from the old one")
    
    async with mysql_client.cursor() as cursor:
        await cursor.push("UPDATE trainer_profiles SET bio = %s WHERE id = %s", (new_bio, user_data.uid,))
    
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.post("/trainer-profile",
    status_code=status.HTTP_201_CREATED, 
    summary="Create trainer bio",
    responses=RESPONSES["POST"]["/trainer-profile"]
)
async def create_trainer_bio(data: TrainerBioOnly, user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Validation trainer bio.
    2. Authentication.
    3. If user is already trainer -> 409.
    4. Create trainer bio in the database.
    5. Return 201 success.
    """
    user_id = user_data.uid

    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT * FROM trainer_profiles WHERE user_id = %s", (user_id,))

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Trainer profile already exists"
            )
        
        balance = 0

        await cursor.push("INSERT INTO trainer_profiles (user_id, bio, balance) VALUES (%s, %s, %s)", (user_id, data.trainer_bio, balance,))


    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Success"}
    )