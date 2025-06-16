from database import mysql_client

async def expired_token_callback(expired_key: str) -> None:
    # getting login_id from key in redis due to format "whitelist:{login_id}"
    login_id = int(expired_key.split(":")[1])
    # update info in db
    async with mysql_client.cursor() as cursor:
        await cursor.push("UPDATE login_activity SET logout_at = NOW(), logout_status = %s WHERE id = %s", 
                          ('expired', login_id,))
    