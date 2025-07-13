from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []
users = {}

class RegisterUser(BaseModel):
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    username: str
    message: str

@app.post("/register")
def register(user: RegisterUser):
    if user.username in users:
        return {"status": "fail", "reason": "User already exists"}
    users[user.username] = user.password
    return {"status": "success"}

@app.post("/login")
def login(user: LoginUser):
    if users.get(user.username) == user.password:
        return {"status": "success"}
    return {"status": "fail", "reason": "Invalid credentials"}

@app.post("/send_message")
def send_message(msg: Message):
    messages.append({
        "username": msg.username,
        "message": msg.message,
        "timestamp": str(datetime.datetime.utcnow())
    })
    return {"status": "sent"}

@app.get("/get_messages")
def get_messages():
    return {"messages": messages}
