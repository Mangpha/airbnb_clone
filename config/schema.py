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


schema = strawberry.Schema(query=Query)
