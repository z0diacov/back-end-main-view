#fastapi
from fastapi import APIRouter, HTTPException, status, Request, BackgroundTasks, Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
#security
from security.jwt import jwt_handler
from security.hash import verify_password, hash_password
from security.config import RESET_PASSWORD_TOKEN_EXPIRE_SECONDS, REFRESH_TOKEN_EXPIRE_SECONDS, EMAIL_CONFIRM_TOKEN_EXPIRE_SECONDS
from schemas.jwt import JWTVerifyEmail, JWTResetPassword, JWTAccess, JWTRefresh
#schemas
from schemas.authorization import LoginData, TwoTokensResponse, AccessTokenResponse, CreatedUserResponse, UserCreate, Forgot_password, Reset_password, EmailStr, GoogleCreatedUserResponse, UrlResponse, GoogleCreatedUserData, FromGoogleUserData, GoogleCallbackData
#database
from database import mysql_client, redis_client
#datetime
from datetime import timedelta
#documentation
from documentation.authorization_responses import RESPONSES
#other
from utils.location.get_location import log_location_activity
from typing import Annotated, Union
from security.authentication import UserDataFromToken, auth_dependences
from service import mailer
from utils.Google_OAuth.google_oauth import google_OAuth
from utils.generators.generator import create_random_number_string
from utils.transcription.transctiption import transcript_to_eng

router = APIRouter()

@router.post("/login",
    status_code=status.HTTP_200_OK,          
    response_model=TwoTokensResponse,
    summary="Login User", 
    responses=RESPONSES["POST"]["/login"]
)
async def login(request: Request, background_tasks: BackgroundTasks, data: LoginData):
    """
    Authenticate the user and generate jwt_handler tokens for access and refresh.

    **Steps:**
    1. Validate user input using Pydantic.
    2. Verify user existence in the database.
    3. Ensure the user's email is verified.
    4. Compare the provided password hash with the stored hash.
    5. Generate `access_token` and `refresh_token` with user `id` and `username`.
    """
    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT * FROM users WHERE username = %s", (data.username,))

    if not user or not verify_password(user[0]["password"], data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    if not user[0]["email_verified"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")
    
    async with mysql_client.cursor() as cursor:
        await cursor.push("INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)", (user[0]['id'], 'classic',))
        last_id = cursor.lastrowid

    access_token = jwt_handler.create_access_token({"uid": user[0]["id"], "sub": data.username, "family": last_id, "iter": 1})
    refresh_token = jwt_handler.create_refresh_token({"uid": user[0]["id"], "sub": data.username, "family": last_id, "iter": 1})

    await redis_client.set(f"whitelist:{last_id}", "1", REFRESH_TOKEN_EXPIRE_SECONDS)

    background_tasks.add_task(log_location_activity, request, last_id, 'login')

    return TwoTokensResponse(
        access_token=access_token, 
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh",
    status_code=status.HTTP_200_OK,          
    response_model=TwoTokensResponse,
    summary="Update access + refresh token", 
    responses=RESPONSES["POST"]["/refresh"]
)
async def refresh(refresh_token: str):
    """
    Authenticate the user and generate a new jwt_handler for access + refresh by not expired refresh.

    **Steps:**
    1. Decode refresh token
    2. Verify user existence in the database.
    3. Verify token validation (iter)
    4. Generate `access_token` + `refresh_token` with user ID, username, family, iter.
    """
    payload = jwt_handler.decode_token(refresh_token, JWTRefresh)

    user_id = payload.uid
    username = payload.sub
    family = payload.family
    iter = payload.iter

    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT * FROM users WHERE id = %s AND username = %s", (user_id, username,)) #checking id and username at the same time

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="User does not exist")

    last_iter_from_redis = await redis_client.get(f"whitelist:{family}")

    if not last_iter_from_redis:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token") #logged out already
    
    if int(last_iter_from_redis) != iter: #logout (strange activity)
        await redis_client.delete(f"whitelist:{family}")
        
        async with mysql_client.cursor() as cursor:
            await cursor.push("""UPDATE login_activity SET logout_at = NOW(), logout_status = %s
                              WHERE id = %s """, ('strange', family))

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail="User must relogin")
    
    access_token = jwt_handler.create_access_token({"uid": user_id, "sub": username, "family": family, "iter": iter + 1})
    refresh_token = jwt_handler.create_refresh_token({"uid": user_id, "sub": username, "family": family, "iter": iter + 1},
                                                      jwt_handler.get_token_seconds_to_expiry(refresh_token))

    await redis_client.set(f"whitelist:{family}", str(iter + 1), jwt_handler.get_token_seconds_to_expiry(refresh_token))

    return TwoTokensResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CreatedUserResponse,
    summary="Create a new user",
    responses=RESPONSES["POST"]["/register"]
)
async def register_user(user: UserCreate):
    """
    Registrate the user and return user data

    **Steps:**
    1. Validate all data
    2. Verify user existence in the database
    3. Verify email existence in the database
    4. Send confirmation mail with url
    4. Put all user data into the database
    """
    async with mysql_client.cursor() as cursor:
        pull_by_username = await cursor.pull("SELECT * FROM users WHERE username = %s", (user.username,))

    if pull_by_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    async with mysql_client.cursor() as cursor:
        pull_by_email = await cursor.pull("SELECT * FROM users WHERE email = %s", (user.email,))

    if pull_by_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        
    async with mysql_client.cursor() as cursor:
        await cursor.push(
            "INSERT INTO users (username, password, email, name) VALUES (%s, %s, %s, %s)", (
                user.username, 
                hash_password(user.password), 
                user.email, 
                user.name,
            )
        )
        user_id = cursor.lastrowid

        await cursor.push("INSERT INTO verify_email_activity (user_id) VALUES (%s)", (user_id,))
        last_id = cursor.lastrowid

    token = jwt_handler.create_token({"email": user.email, "family": last_id}, EMAIL_CONFIRM_TOKEN_EXPIRE_SECONDS, JWTVerifyEmail)
    email_verification_url = f"http://localhost:3000/auth/verify-email?token={token}"

    print(f"{email_verification_url=}")

    await mailer.send_email(
        message_type=JWTVerifyEmail.model_fields["type"].default,
        recipient=user.email,
        data={'button_link': email_verification_url}
    )

    return CreatedUserResponse(
        username=user.username,
        email=user.email,
        name=user.name
    )

@router.post("/verify-email-link",
    status_code=status.HTTP_200_OK,
    summary="Creates verify link token",
    responses=RESPONSES["POST"]["/verify-email-link"]
)
async def verify_email_link(email: EmailStr = Query(...)):
    """
    **Steps:**
    1. Validate email by pydantic
    2. Verify email existence in the database
    3. If email alredy confirmed -> 409
    4. Create token
    5. Send confirmation mail with url
    6. Return result
    """
    async with mysql_client.cursor() as cursor:
        user_data = await cursor.pull("SELECT id, email_verified FROM users WHERE email = %s", (email,))

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

    user_id = user_data[0]["id"]
    if user_data[0]["email_verified"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="The email has already been verified")

    token = jwt_handler.create_token({"email": email, "family": user_id}, EMAIL_CONFIRM_TOKEN_EXPIRE_SECONDS, JWTVerifyEmail)
    email_verification_url = f"http://localhost:3000/auth/verify-email?token={token}"

    print(f"{email_verification_url=}")

    await mailer.send_email(
        message_type=JWTVerifyEmail.model_fields["type"].default,
        recipient=email,
        data={'button_link': email_verification_url}
    )

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"detail": "Success"})

@router.post("/verify-email",
    status_code=status.HTTP_200_OK,
    summary="Verify user's email via link",
    responses=RESPONSES["POST"]["/verify-email"]
)
async def verify_email(request: Request, background_tasks: BackgroundTasks, token: str = Query(...)):
    """
    Verify user's email using the provided token.

    **Steps:**
    1. Extract and validate the token.
    - If expired or invalid, return 401 with the error message.
    2. Check if the user exists:
    - If not found, return 404.
    3. If valid, update user status to "verified".
    4. If email is already verified, return 409.
    5. Returns 200 OK.
    """
    payload = jwt_handler.decode_token(token, JWTVerifyEmail)

    email = payload.email
    family = payload.family

    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT * FROM users WHERE email = %s", (email,))
        
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
    
    if user[0]["email_verified"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="The email has already been verified")
        
    async with mysql_client.cursor() as cursor:
        await cursor.push("UPDATE users SET email_verified = 1 WHERE email = %s", (email,))
        await cursor.push("UPDATE verify_email_activity SET verified_at = NOW() WHERE id = %s", (family,))

    background_tasks.add_task(log_location_activity, request, family, 'verify_email')

    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.post("/forgot-password", 
    status_code=status.HTTP_200_OK, 
    summary="Request a password reset link",
    responses=RESPONSES["POST"]["/forgot-password"]
)
async def forgot_password(data: Forgot_password):
    """
    Generate a password reset link for the user.

    **Steps:**
    1. Validate the email format.
    2. Check if the user exists with the provided email:
    - If not found, return 404.
    3. Create a token with expiration.
    4. Check redis
    5. Statistic
    6. Send an email with the reset link to the user.
    """

    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT * FROM users WHERE email = %s", (data.email,))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not user[0]["email_verified"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")
    
    async with mysql_client.cursor() as cursor:
        await cursor.execute("INSERT INTO reset_password_activity (user_id, is_used) VALUES (%s, %s)", (user[0]['id'], False,))
        last_id = int(cursor.lastrowid)

    token = jwt_handler.create_token({"email": data.email, "family": last_id}, RESET_PASSWORD_TOKEN_EXPIRE_SECONDS, JWTResetPassword)
    reset_password_url = f"http://localhost:3000/auth/reset-pass?token={token}"

    print(f"{reset_password_url=}")

    await mailer.send_email(
        message_type=JWTResetPassword.model_fields["type"].default,
        recipient=data.email,
        data={'button_link': reset_password_url}
    )

    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.put("/password-forgot", 
    status_code=status.HTTP_200_OK, 
    summary="Reset the user's password",
    responses=RESPONSES["PUT"]["/password-forgot"]
)
async def reset_password(request: Request, data: Reset_password, background_tasks: BackgroundTasks):
    """
    Reset the user's password using the provided reset token.

    **Steps:**
    1. Validate password
    2. Validate the reset token:
    - If invalid or expired, return 401.
    3. Check if the user exists:
    - If not found, return 404.
    4. Ensure the new password is different from the current password:
    - If the same, return 409.
    5. Update the user's password and return success.
    """  
    payload = jwt_handler.decode_token(data.token, JWTResetPassword)

    email = payload.email
    family = payload.family

    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT * FROM users WHERE email = %s", (email,))
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Email not found")
    
    if not user[0]["email_verified"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Email not verified")

    if verify_password(user[0]["password"], data.new_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="New password must be different from the old one")

    if await redis_client.exists(f"reset_password:{family}"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Already used token")
    else:
        await redis_client.set(f"reset_password:{family}", "1", jwt_handler.get_token_seconds_to_expiry(data.token))
        
    async with mysql_client.cursor() as cursor:
        await cursor.push("UPDATE users SET password = %s WHERE email = %s",
                    (hash_password(data.new_password), email))

        await cursor.push(
            """UPDATE reset_password_activity SET  
               is_used = 1, reset_at = NOW() WHERE id = %s""",
            (family,)
        )

    background_tasks.add_task(log_location_activity, request, family, 'reset_password')

    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.post("/logout", #authorization
    status_code=status.HTTP_200_OK, 
    summary="Logout, close session",
    responses=RESPONSES["POST"]["/logout"]
)
async def logout(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication + validation data from `access`.
    2. Close token family (close session).
    3. Return result 
    """

    family = user_data.family
    
    await redis_client.delete(f"whitelist:{family}") #close session
    
    async with mysql_client.cursor() as cursor:
        await cursor.push("""
        UPDATE login_activity SET logout_at = NOW(),
        logout_status = %s WHERE id = %s
        """, ('self', family,))

    return JSONResponse(status_code=status.HTTP_200_OK, 
                    content={"detail": "Success"})
    
#Google OAuth
#url: https://accounts.google.com/o/oauth2/auth?client_id=878938130217-4ua6ncsu7ff9saqhfr889jjm21rqd1m6.apps.googleusercontent.com&response_type=code&redirect_uri=http://localhost:8000/google/auth/callback&scope=openid%20email%20profile
@router.post("/google/auth/callback",
            status_code=status.HTTP_200_OK,
            response_model=Union[
                TwoTokensResponse,
                GoogleCreatedUserResponse
            ],
            summary="Login or register user (nonexist email) via google account",
            responses=RESPONSES["POST"]["/google/auth/callback"])
async def google_callback(request: Request, background_tasks: BackgroundTasks, data: GoogleCallbackData):
    """
    Steps:
    1. Get user data by code
    2. Check user email in db. If exists -> login, else -> registration
    3. If it is login create access and refresh and return -> 200 + whitelist
    4. If it is registration check username(email without domain) exists in db
    5. If exists generate random  in 20 numerals on conflict retry
    6. Return 201 with user data and access and refresh + whitelist
    """
    code = data.code
    google_user_data: dict = await google_OAuth.get_user_data(code)

    user_data: FromGoogleUserData = FromGoogleUserData(
        email=google_user_data['email'],
        name=google_user_data['given_name']
    )

    async with mysql_client.cursor() as cursor:
        user = await cursor.pull("SELECT id, username, email_verified FROM users WHERE email = %s",
                    (user_data.email,))
        
    is_registration: bool = False
    created_user_data: Union[None, GoogleCreatedUserData] = None #for global vision

    if not user: #user does not exist -> registartion()
        is_registration = True
        username = user_data.email.split("@")[0].replace('.', '')[:50]
        """
        Google can return not only english names
        Steps: 
        1. Transcript to english
        2. Check length, if > 50 -> name = None (name is not necessary row)
        3. Validate it like in /register, if Validation error -> name = None
        """
        english_name = transcript_to_eng(user_data.name)

        if len(english_name) > 50:
            english_name = None

        async with mysql_client.cursor() as cursor:
            username_exists = await cursor.pull("SELECT id FROM users WHERE username = %s",
                        (username,))
        
        while username_exists:
            async with mysql_client.cursor() as cursor:
                username_exists = await cursor.pull("SELECT id FROM users WHERE username = %s",
                            (username := create_random_number_string(20)))
                    
        async with mysql_client.cursor() as cursor:
            await cursor.push(
                "INSERT INTO users (username, email, name, email_verified) VALUES (%s, %s, %s, %s)", (
                    username,
                    user_data.email, 
                    english_name,
                    1,
                )
            )
            user_id = cursor.lastrowid
        try:
            created_user_data = GoogleCreatedUserData(
                username=username,
                email=user_data.email,
                name=english_name
            )
        except ValueError:
            created_user_data = GoogleCreatedUserData(
                username=username,
                email=user_data.email,
                name=None
            )
    else:
        user_id = user[0]['id']
        username = user[0]['username']
        email_verified = user[0]['email_verified']

    #login
    async with mysql_client.cursor() as cursor:
            await cursor.push("INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)", (user_id, 'google',))
            last_id = cursor.lastrowid

            if not email_verified: #email_verified = 1 if user signed in with google after not confirming the email
                await cursor.push("UPDATE users SET email_verified = 1 WHERE id = %s", (user_id,))


    access_token = jwt_handler.create_access_token({"uid": user_id, "sub": username, "family": last_id, "iter": 1})
    refresh_token = jwt_handler.create_refresh_token({"uid": user_id, "sub": username, "family": last_id, "iter": 1})

    await redis_client.set(f"whitelist:{last_id}", "1", REFRESH_TOKEN_EXPIRE_SECONDS)

    background_tasks.add_task(log_location_activity, request, last_id, 'login')

    two_tokens_response: TwoTokensResponse = TwoTokensResponse(
        access_token=access_token, 
        refresh_token=refresh_token,
        token_type="bearer"
    )

    if not is_registration:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content = two_tokens_response.model_dump()
        )

    else:    
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=GoogleCreatedUserResponse(
                user_data=created_user_data,
                tokens=two_tokens_response
            ).model_dump()
        )
