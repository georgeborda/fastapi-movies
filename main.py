from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

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

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "1.1"


@app.get('/', tags = ["home"])
def message():
    return HTMLResponse('<h1>Hello world</h1>')
# Retorna hola mundo con formato de HTML, en este caso un título


@app.get('/movies', tags =["movies"], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)
# Retorna el arreglo con todas las películas


# PARÁMETROS DE RUTA - Busca el id
@app.get('/movies/{id}', tags = ['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: 
# Parametro de ruta: id
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])
# De acuerdo al id ingresado imprime los datos de la película con dicho id


# PARÁMETRO QUERY - Filtra por categoría
@app.get('/movies/', tags = ['movies'], response_model=List[Movie])
# Se coloca / después de /movies para que no se sobreescriba el que ya se había generado más arriba, sino que sea una ruta diferente
def get_movies_by_category(category: str = Query(min_length=5, max_length=30), year: int = Query(le=2023)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category and int(item['year']) == year]  # Modo inline
    return JSONResponse(content=data)
# La diferencia con los parámetros de ruta está en que en este no se especifica el parámetro en la url "'/movies/{id}'" vs "'/movies/'"


@app.post('/movies', tags= ['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={'message': 'Se ha registrado la película'})


@app.put('/movies', tags = ['movies'], response_model=dict)
def update_movie(id: int, movie: Movie ) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return JSONResponse(content={'message': 'Se ha modificado la película'})


@app.delete('/movies', tags = ['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(content={'message': 'Se ha eliminado la película'})