from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):# Se genera una función asyncrona puesto que la respuesta por parte del usuario puede tardar
        # Request viene desde FastAPI
        auth = await super().__call__(request)
        # __call__ es un método de HTTPBearer y retorna las credenciales
        # Se utiliza await ya que este proceso podría demorar por respuesta del usuario
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son inválidas")