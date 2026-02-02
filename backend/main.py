from typing import Annotated
from datetime import timedelta
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    get_user,
    verify_password,
    Token,
    User as AuthUser # Alias to avoid conflict with DBUser
)
from .src.database import get_db
from .src.schemas import UserCreate, UserUpdate, User as UserSchema
from .src.models import User as DBUser # Alias for the SQLAlchemy model


app = FastAPI(
    title="Corexus Backend",
    description="The FastAPI backend for the Corexus intelligent assistant.",
    version="0.1.0",
)

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserSchema)
async def read_users_me(current_user: Annotated[DBUser, Depends(get_current_active_user)]):
    return current_user

@app.get("/")
async def root():
    # Triggering rebuild for Heroku cache clear
    return {"message": "Welcome to Corexus Backend!"}

@app.get("/status")
async def get_status():
    return {"status": "operational", "version": app.version}

@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        email=user.email, 
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Authorization check (optional: restrict to self or admin)
    # if db_user.id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to update this user")

    update_data = user_update.model_dump(exclude_unset=True)
    if 'password' in update_data:
        hashed_password = get_password_hash(update_data['password'])
        update_data['hashed_password'] = hashed_password
        del update_data['password']
        
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_user)
):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Authorization check
    # if db_user.id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    db.delete(db_user)
    db.commit()
    return None

@app.get("/users/", response_model=list[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(DBUser).offset(skip).limit(limit).all()
    return users

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
