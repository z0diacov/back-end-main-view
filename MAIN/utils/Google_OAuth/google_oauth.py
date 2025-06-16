import httpx
from fastapi import HTTPException, status
from security.config import GOOGLE_OAUTH_CONFIG

class GoogleOAuth():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        if not hasattr(self, '__initialized'):
            self.client_secret = GOOGLE_OAUTH_CONFIG['client_secret']
            self.client_id = GOOGLE_OAUTH_CONFIG['client_id']
            self.redirect_uri = GOOGLE_OAUTH_CONFIG['redirect_uri']
            self.__initialized = True
    
    def create_auth_url(self) -> str:
        google_auth_url: str = (
            "https://accounts.google.com/o/oauth2/auth?"
            f"client_id={self.client_id}"
            "&response_type=code"
            f"&redirect_uri={self.redirect_uri}"
            "&scope=openid%20email%20profile"
        )
        return google_auth_url
    
    async def get_user_data(self, code: str) -> dict:
        token_url = "https://oauth2.googleapis.com/token"

        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                token_url,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri,
                },
            )
            token_data = token_response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Invalid token")

            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            userinfo_response = await client.get(
                userinfo_url, headers={"Authorization": f"Bearer {access_token}"}
            )
            userinfo = userinfo_response.json()
            return userinfo
        
google_OAuth = GoogleOAuth()