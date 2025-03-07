from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/users', response_model=List[User])
def get_users():
    return users

@app.post('/user/{username}/{age}', response_model=User )
def create_user(username: str, age: int):
    user_id = (users[-1].id + 1) if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}', response_model=User)
def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='Пользователь не найден')

@app.delete('/user/{user_id}', response_model=User)
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='Пользователь не найден')