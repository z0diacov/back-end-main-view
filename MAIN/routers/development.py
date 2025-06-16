from fastapi import APIRouter, HTTPException, status, Request, Depends, Query, File, UploadFile
from fastapi.responses import JSONResponse

from schemas.authentication import UserDataFromToken
from documentation.authorization_responses import RESPONSES as AUTHRESPONSE
from documentation.session_responses import RESPONSES as SESSRESPONSE

from security.config import RABBIT_QUEUES

from database import redis_client, mysql_client
from rabbitmq import rabbitmq_client
from security.authentication import auth_dependences
from security.otp import otp_client

from security.config import AVARAR_SIZE_LINIT_IN_BYTES, ALLOWED_AVARAR_TYPES

router = APIRouter()

@router.get("/brocker-message")
async def brocker_message(message: str):
    await rabbitmq_client.publish(RABBIT_QUEUES['to_mailer'], {'message': message})

@router.post("/avatrar")
async def file_upload(file: UploadFile = File(...)):
    contents = await file.read()

    if not contents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="File is empty")
    
    if file.content_type not in ALLOWED_AVARAR_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Unsupported file type")
    
    if file.size > AVARAR_SIZE_LINIT_IN_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="File size exceeds limit")
    
    await rabbitmq_client.publish(
        RABBIT_QUEUES['to_media'], {
            'type': 'avatar', 
            'filename': file.filename, 
            'content_type': file.content_type, 
            'size': len(contents)
        }
    )

    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"detail": "Success"})

@router.post("/otp")
async def create_otp(user_data: UserDataFromToken = Depends(auth_dependences.required_auth)):

    user_id = user_data.uid

    otp = await otp_client.set_otp(user_id, sending_method='email')

    print(otp)
    
    return JSONResponse(status_code=status.HTTP_200_OK, 
                        content={"delail": "Success"})

@router.post(
    "/verify-otp",
    response_model=UserDataFromToken,
    status_code=status.HTTP_200_OK,
    summary="Verify OTP"
)
async def verify_otp(user_data: UserDataFromToken = Depends(auth_dependences.otp_auth)) -> UserDataFromToken:
    return user_data