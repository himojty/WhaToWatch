from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result

from core.models import Movie
from core.schemas.movies import (
    MovieUpdate,
    MovieUpdatePartial,
    MovieCreate,
)


async def create_movie(session: AsyncSession, movie_in: MovieCreate) -> Movie:
    movie = Movie(**movie_in.model_dump())
    session.add(movie)
    await session.commit()
    return movie


async def get_movies(session: AsyncSession) -> list[Movie] | None:
    stmt = select(Movie).order_by(Movie.id)
    result: Result = await session.execute(stmt)
    movies = result.scalars().all()
    return movies


async def get_movie(session: AsyncSession, movie_id: int) -> Movie | None:
    return await session.get(Movie, movie_id)


async def update_movie(
    session: AsyncSession,
    movie: Movie,
    movie_update: MovieUpdate | MovieUpdatePartial,
    partial: bool = False,
) -> MovieUpdate:
    for name, value in movie_update.model_dump(exclude_unset=partial).items():
        setattr(movie, name, value)
    await session.commit()
    return movie_update


async def delete_movie(session: AsyncSession, movie: Movie) -> None:
    await session.delete(movie)
    await session.commit()
