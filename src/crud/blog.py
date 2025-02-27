from fastapi import Depends
from sqlalchemy.orm import Session

from src.exceptions import BlogNotFoundError, UnauthorizedError
from src.models.blog import Blog as BlogModel
from src.schemas.blog import Blog
from src.schemas.user import User
from src.utils.oauth2 import get_current_user


def get_all(db: Session):
    blogs = db.query(BlogModel).all()
    return blogs


def create(request: Blog, db: Session, current_user: User):
    new_blog = BlogModel(title=request.title, description=request.description, user_id=current_user.id)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def delete(blog_id: int, db: Session, current_user: User):
    my_blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()

    if not my_blog:
        raise BlogNotFoundError(f"Blog {blog_id} not found")

    if current_user.is_admin or my_blog.written_by == current_user:
        db.delete(my_blog)
        db.commit()
        return {"message": "Blog deleted successfully"}

    raise UnauthorizedError(f"User {current_user.username} is not authorized to delete this blog")


def update(blog_id: int, request: Blog, db: Session, current_user: User = Depends(get_current_user)):
    my_blog = db.query(BlogModel).filter(BlogModel.id == blog_id)
    blog_instance = my_blog.first()

    if blog_instance is None:
        raise BlogNotFoundError(f"Blog {blog_id} not found")

    if blog_instance.written_by.username != current_user.username:
        raise UnauthorizedError(f"User {current_user.username} is not authorized to update a blog for another person")

    my_blog.update(request.model_dump())
    db.commit()
    return {"message": "Blog updated successfully"}


def get(blog_id: int, db: Session):
    my_blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()
    if not my_blog:
        raise BlogNotFoundError(f"Blog {blog_id} not found")
    return my_blog
