from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    # ahora creamos el método que se va a estar ejecutando para ver si se genera un error en la aplicación
    async def dispatch(self, request: Request, call_next):
    # call_next es para que si no se genera un error, ejecute la siguiente acción
        try: 
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})