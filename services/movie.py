from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_category(self, category, year):
        result = self.db.query(MovieModel).filter(MovieModel.category == category and MovieModel.year == year).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id: int, data:Movie):
        modify_movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        modify_movie.title = data.title
        modify_movie.overview = data.overview
        modify_movie.year = data.year
        modify_movie.rating = data.rating
        modify_movie.category = data.category
        self.db.commit()
        return
    
    def delete_movie(self, movie):
        self.db.delete(movie)
        self.db.commit()
        return
