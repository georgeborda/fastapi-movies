# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.login import login_router


app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "1.1"

app.add_middleware(ErrorHandler)
# FastAPI permite agregar un middleware a nivel de todo la aplicación con add_middleware
app.include_router(movie_router)
app.include_router(login_router)


Base.metadata.create_all(bind=engine)



@app.get('/', tags = ["home"])
def message():
    return HTMLResponse('<h1>Hello world</h1>')
# Retorna hola mundo con formato de HTML, en este caso un título




