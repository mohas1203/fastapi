from starlette import status
from app import models, schemas
from app.database import get_db
from app.utils import hash_password
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter


router = APIRouter(prefix="/users", tags=['Users'])


# Route to create new user
@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash password
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get User Data
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} was not found")

    return user
