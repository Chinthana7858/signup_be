from fastapi import FastAPI, HTTPException, Depends
from models import UserLogin, UserSignUp
from database import user_collection
from fastapi.middleware.cors import CORSMiddleware
from utils.security import pwd_context
from utils.jwt import create_access_token
from utils.security import hash_password

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup")
async def signup(user: UserSignUp):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if await user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password) 
    user_dict.pop("confirm_password")  

    await user_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

@app.post("/signin")
async def signin(user: UserLogin):
    db_user = await user_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}

#uvicorn main:app --reload
