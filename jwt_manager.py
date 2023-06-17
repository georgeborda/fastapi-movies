from jwt import encode, decode
from dotenv import load_dotenv
import os

load_dotenv()

def create_token(data: dict) -> str:
    token: str = encode(payload=data,
                        key=os.getenv('SECRET_KEY'),
                        algorithm="HS256"
                        )
    return token

def validate_token(token: str) -> dict:
    data : dict = decode(token, key=os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return data