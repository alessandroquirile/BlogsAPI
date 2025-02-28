from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.crud import blog
from src.exceptions import UnauthorizedError
from src.schemas.blog import Blog, ShowBlog
from src.schemas.user import User
from src.utils.database import get_db
from src.utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


# Remove the "/" for avoiding redirect loop!
@router.get("", response_model=List[ShowBlog])
async def blogs(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.get("/{blog_id}", response_model=ShowBlog)
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return blog.get(blog_id, db)


@router.post("/create-blog", status_code=status.HTTP_201_CREATED)
async def create_blog(request: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise UnauthorizedError
    return blog.create(request, db, current_user)


@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_blog(blog_id: int, request: Blog, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    if not current_user:
        raise UnauthorizedError
    return blog.update(blog_id, request, db, current_user)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise UnauthorizedError
    return blog.delete(blog_id, db, current_user)
