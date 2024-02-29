from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = [
    {   
        "id": 1,
        "name": "John",
        "age": 28
    },
    {
        "id": 2,
        "name": "Jane",
        "age": 32
    },
    {
        "id": 3,
        "name": "Doe",
        "age": 45
    },
    {
        "id": 4,
        "name": "Smith",
        "age": 22
    }
]

class RootReturnObj(BaseModel):
    Hello: str

@app.get("/")
async def helloWorld() -> RootReturnObj:
    return {"Hello": "World"}


@app.get("/say-hello-john")
async def helloJohn():
    return "Hello John!"


class User(BaseModel):
    id: int
    name: str
    age: int


@app.get("/users")
async def getUsers() -> list[User]:
    """
    Endpoint to return all users
    """
    return users

@app.get("/users/{user_id}", responses={404: {"model": str}})
async def getUser(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


film = [
    {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "year": 1994
    },
    {
        "title": "The Godfather",
        "director": "Francis Ford Coppola",
        "year": 1972
    },
    {
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "year": 2008
    },
    {
        "title": "The Godfather: Part II",
        "director": "Francis Ford Coppola",
        "year": 1974
    },
    {
        "title": "Anatomie d'une chute",
        "director": "Justine Triet",
        "year": 2023
    },
    {
        "title": "Past lives",
        "director": "Celine Song",
        "year": 2023
    }
    
]

@app.get("/films")
async def getFilmsByParameters(title: str | None = '', director: str | None = '', year: str | None = '') -> List[dict]:

    filtered_films = []
    for f in film:
        if (title is None or f["title"].lower() == title.lower()) and \
           (director is None or f["director"].lower() == director.lower()) and \
           (year is None or f["year"] == year):
            filtered_films.append(f)
    return filtered_films


class Film(BaseModel):
    title: str = ""
    director: str = ""
    year: int = 0


@app.post("/films/filter")
async def filterFilmsByParameters(films_filter: Film) -> List[dict]:
    filtered_films = []
    for f in film:
        if (films_filter.title is None or f["title"].lower() == films_filter.title.lower()) or \
           (films_filter.director is None or f["director"].lower() == films_filter.director.lower()) or \
           (films_filter.year is None or f["year"] == films_filter.year):
            filtered_films.append(f)
    return filtered_films

@app.post("/users")
async def addUser(user: User) -> User:
    users.append(user.dict())
    return user

@app.delete("/users/{user_id}")
async def deleteUser(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.put("/users/{user_id}")
async def updateUser(user_id: int, user: User) -> User:
    for u in users:
        if u["id"] == user_id:
            u["name"] = user.name
            u["age"] = user.age
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

