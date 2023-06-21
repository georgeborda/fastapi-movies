# Python
from typing import Optional, List

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder

from jwt_manager import create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel


app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "1.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):# Se genera una función asyncrona puesto que la respuesta por parte del usuario puede tardar
        # Request viene desde FastAPI
        auth = await super().__call__(request)
        # __call__ es un método de HTTPBearer y retorna las credenciales
        # Se utiliza await ya que este proceso podría demorar por respuesta del usuario
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son inválidas")

# Models

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }

movies = [
    {
        "id" : 1,
        "title" : "Avatar",
        "overview" : "En un exuberante planeta llamado Pandora viven...",
        "year" : "2009",
        "rating" : 7.8,
        "category" : "Acción",
    },
    {
        "id" : 2,
        "title" : "Avatar",
        "overview" : "En un exuberante planeta llamado Pandora viven...",
        "year" : "2009",
        "rating" : 7.8,
        "category" : "Acción",
    }
]


@app.get('/', tags = ["home"])
def message():
    return HTMLResponse('<h1>Hello world</h1>')
# Retorna hola mundo con formato de HTML, en este caso un título

@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token : str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags =["movies"], response_model=List[Movie], status_code=200, dependencies= [Depends(JWTBearer())])
# dependencies hace que requiera autenticación para ejecutar este endpoint
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))



# PARÁMETROS DE RUTA - Busca el id
@app.get('/movies/{id}', tags = ['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: 
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    # Se hace el filtrado por el id y como es único, colocamos first para que no continue buscando
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
# De acuerdo al id ingresado imprime los datos de la película con dicho id


# PARÁMETRO QUERY - Filtra por categoría
@app.get('/movies/', tags = ['movies'], response_model=List[Movie], status_code=200)
# Se coloca / después de /movies para que no se sobreescriba el que ya se había generado más arriba, sino que sea una ruta diferente
def get_movies_by_category(category: str = Query(min_length=5, max_length=30), year: int = Query(le=2023)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category and MovieModel.year == year).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
# La diferencia con los parámetros de ruta está en que en este no se especifica el parámetro en la url "'/movies/{id}'" vs "'/movies/'"


@app.post('/movies', tags= ['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict()) # ** hace que movie.dict() se ingresen como parámetros a MovieModel
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={'message': 'Se ha registrado la película'})


@app.put('/movies', tags = ['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie ) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado la película'})


@app.delete('/movies', tags = ['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha eliminado la película'})