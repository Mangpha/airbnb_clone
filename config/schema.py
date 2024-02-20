from typing import List

import strawberry


@strawberry.type
class Movie:
    id: int
    title: str
    year: int
    rating: float


movies_db = [
    Movie(id=1, title="test", year=2020, rating=4.5),
]


@strawberry.type
class Query:

    @strawberry.field
    def movies(self) -> List[Movie]:
        return movies_db

    @strawberry.field
    def movie(self, movie_id: int) -> Movie:
        return movies_db[movie_id - 1]


@strawberry.type
class Mutation:

    @strawberry.field
    def add_movie(self, title: str, year: int, rating: float) -> Movie:
        new_movie = Movie(id=len(movies_db) + 1, title=title, year=year, rating=rating)
        movies_db.append(new_movie)
        return new_movie


schema = strawberry.Schema(query=Query, mutation=Mutation)
