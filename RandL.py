# generating a register and login using fastapi()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

# Create FastAPI instance
app = FastAPI()

# Create password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake database (dictionary)
users_db = {"username":"abc"}

# Define User model
class User(BaseModel):
    username: str
    password: str


# Route ⿡: Register user
@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password before saving
    # hashed_password = pwd_context.hash(user.password)
    # users_db[user.username] = hashed_password
    return {"message": f"User '{user.username}' registered successfully"}


# Route ⿢: Login user
@app.post("/login")
def login(user: User):
    if user.username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = users_db[user.username]
    if not pwd_context.verify(user.password, stored_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": f"Welcome back, {user.username}!"}

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI! Use /register or /login endpoints."}