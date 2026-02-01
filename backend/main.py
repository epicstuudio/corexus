from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn

from .auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    fake_users_db,
    get_current_active_user,
    get_password_hash,
    get_user,
    verify_password,
    User,
    Token,
)

app = FastAPI(
    title="Corexus Backend",
    description="The FastAPI backend for the Corexus intelligent assistant.",
    version="0.1.0",
)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.get("/")
async def root():
    return {"message": "Welcome to Corexus Backend!"}

@app.get("/status")
async def get_status():
    return {"status": "operational", "version": app.version}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Initial comment
# Another comment to trigger deployment
# Another trigger for backend
# Yet another trigger for backend
# Trigger for new backend app deployment
# Trigger for explicit force push
