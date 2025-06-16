import httpx
from fastapi import Request
from utils.user_agent_data.get_data import get_data_by_user_agent
from database import mysql_client
import geoip2.database
from datetime import datetime

def get_location_by_ip(ip: str) -> dict:
    try:
        if ip == "testclient":
            ip = "127.0.0.1"
        with geoip2.database.Reader("utils/location/GeoLite2-City.mmdb") as reader:
            data = reader.city(ip)
            result = {
                "country": getattr(data.country, "name", None),
                "regionName": data.subdivisions.most_specific.name if len(data.subdivisions) > 0 else None,
                "city": getattr(data.city, "name", None),
                "lat": getattr(data.location, "latitude", None),
                "lon": getattr(data.location, "longitude", None)
            }
            return result

    except geoip2.errors.AddressNotFoundError:
        return {
                "country": None,
                "regionName": None,
                "city": None,
                "lat": None,
                "lon": None
            }
    

async def log_location_activity(request: Request, activity_id: int, activity_type: str) -> None:
    ip = request.client.host
    location = get_location_by_ip(ip)
    
    user_agent_string = request.headers.get("User-Agent", "Unknown")
    user_agent_data = get_data_by_user_agent(user_agent_string)

    async with mysql_client.cursor() as cursor:
        await cursor.push("""
            INSERT INTO location_activity 
            (ip, location_country, location_region, location_city, location_lat, location_lon, browser, os, device, activity_id, activity_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                ip, 
                location['country'],
                location['regionName'],
                location['city'],
                location['lat'],
                location['lon'],
                *user_agent_data,
                activity_id,
                activity_type
            )
        )