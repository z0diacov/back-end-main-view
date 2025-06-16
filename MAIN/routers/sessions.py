#fastapi
from fastapi import APIRouter, HTTPException, status, Request, BackgroundTasks, Security, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
#security
from security.jwt import jwt_handler
from security.hash import verify_password, hash_password
from security.config import EMAIL_CONFIRM_TOKEN_EXPIRE_MINUTES, RESET_PASSWORD_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_SECONDS, RESET_PASSWORD_TOKEN_EXPIRE_SECONDS
from schemas.jwt import JWTVerifyEmail, JWTResetPassword, JWTAccess, JWTRefresh
#schemas
from schemas.sessions import MyActiveSessionsResponse, Session
#database
from database import mysql_client, redis_client
#datetime
from datetime import timedelta
#documentation
from documentation.session_responses import RESPONSES
#auth
from schemas.authentication import UserDataFromToken
#other
from utils.location.get_location import log_location_activity
from security.authentication import auth_dependences

router = APIRouter()

@router.get("/my-active-sessions",
    status_code=status.HTTP_200_OK,          
    response_model=MyActiveSessionsResponse,
    summary="My activce sessions", 
    responses=RESPONSES["GET"]["/my-active-sessions"]
)
async def get_my_active_sessions(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)) -> MyActiveSessionsResponse:
    """
    steps:
    1. Authentication + validation data from `access`.
    2. Find all `family` (`id`) from user.
    3. Check each `family` in `whitelist` (if not includes -> already logged out (not session)).
    4. Otherwise get data from those `family's` from database (table location_activity).
    5. Return all sessions.
    """

    async with mysql_client.cursor() as cursor:
        session_pretendents = await cursor.pull(
            """SELECT id, login_at FROM login_activity 
            WHERE user_id = %s AND logout_at IS NULL""", #todo: 7 days
            (user_data.uid,)
        )

        sessions_ids = [item for item in session_pretendents if await redis_client.exists(f"whitelist:{item['id']}")]

        session_data = await cursor.pull(
            f"""
            SELECT * FROM location_activity
            WHERE activity_id IN ({','.join(['%s'] * len(sessions_ids))}) 
            AND activity_type = 'login'""", 
            tuple(item['id'] for item in sessions_ids)
        )

        return MyActiveSessionsResponse(sessions=[
            Session(**{**item, "login_at": sessions_ids[i]["login_at"], "session_id": sessions_ids[i]["id"]})
            for i, item in enumerate(session_data)
        ])

@router.delete("/session", #sessions
    status_code=status.HTTP_200_OK, 
    summary="Close session",
    responses=RESPONSES["DELETE"]["/session"]
)
async def close_session(session_id: int = Query(...), user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication + validation data from `access`.
    2. Check `session_id` belongs user, if not -> 403.
    3. If 'session_id' = user session (`family`) (can't logout this way) -> 409.
    4. Close token `family` (close session).
    5. Return result.
    """
    user_id = user_data.uid
    family = user_data.family

    async with mysql_client.cursor() as cursor:
        belong_check = await cursor.pull("""
        SELECT 1 FROM login_activity WHERE id = %s AND user_id = %s AND logout_at IS NULL
        """, (session_id, user_id,))

    if not belong_check:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, 
                    content={"detail": "Session does not belong to the authenticated user"})

    if session_id == family:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, 
            content={"detail": "Can't logout user's session this way"})

    await redis_client.delete(f"whitelist:{session_id}")

    return JSONResponse(status_code=status.HTTP_200_OK, 
                content={"detail": "Success"})

@router.delete("/sessions", #sessions
    status_code=status.HTTP_200_OK, 
    summary="Close sessions",
    responses=RESPONSES["DELETE"]["/sessions"]
)
async def close_sessions(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):
    """
    Steps:
    1. Authentication + validation data from `access`.
    2. Close all sessions belong current user (exept current session).
    3. Return result.
    """
    user_id = user_data.uid
    family = user_data.family

    async with mysql_client.cursor() as cursor: #TODO: redis expire event
        sessions = await cursor.pull("""
        SELECT id FROM login_activity WHERE user_id = %s 
        AND logout_at IS NULL AND id != %s
        """, (user_id, family,))

        for item in sessions:
            await redis_client.delete(f"whitelist:{item}")

        #TODO: 2 requests in 1 (???)

        await cursor.push("""
        UPDATE login_activity SET logout_status = %s,
        logout_at = NOW() WHERE user_id = %s 
        AND logout_at IS NULL AND id != %s
        """, ('extra', user_id, family,))

    return JSONResponse(status_code=status.HTTP_200_OK,
                content={"detail": "Success"})
