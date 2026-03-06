from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config import engine, get_db
import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# USERS

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all() # SELECT * FROM users


@app.get("/users/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    # SELECT * FROM users WHERE id = user_id

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")

    db_user = models.User(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
# Insert into users (id, name, email, age) values (user.id, user.name, user.email, user.age)
    return db_user


@app.put("/users/{user_id}")
def update_user(user_id: str, user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # check email trùng với user khác
    existing = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.id != user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already used")

    db_user.name = user.name
    db_user.email = user.email
    db_user.age = user.age

    db.commit()
    db.refresh(db_user)
# UPDATE users SET name = user.name, email = user.email, age = user.age WHERE id = user_id
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
# DELETE FROM users WHERE id = user_id
    return {"detail": "User deleted successfully"}


# Profile

@app.get("/users/{user_id}/profile")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    # SELECT * FROM profiles WHERE user_id = user_id

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@app.post("/users/{user_id}/profile")
def create_profile(user_id: str, profile: schemas.ProfileCreate, db: Session = Depends(get_db)):

    # check user tồn tại
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if db.query(models.Profile).filter(models.Profile.user_id == user_id).first():
        raise HTTPException(status_code=400, detail="Profile for this user already exists")

    db_profile = models.Profile(
        user_id=user_id,
        address=profile.address,
        phone=profile.phone,
        bio=profile.bio
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@app.put("/users/{user_id}/profile")
def update_profile(user_id: str, profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db_profile.address = profile.address
    db_profile.phone = profile.phone
    db_profile.bio = profile.bio

    db.commit()
    db.refresh(db_profile)
    return db_profile


@app.delete("/users/{user_id}/profile")
def delete_profile(user_id: str, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(db_profile)
    db.commit()
    return {"detail": "Profile deleted successfully"}


# POSTS

@app.get("/users/{user_id}/posts")
def get_posts(user_id: str, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    # SELECT * FROM posts WHERE user_id = user_id

    return posts


@app.post("/users/{user_id}/posts")
def create_post(user_id: str, post: schemas.PostCreate, db: Session = Depends(get_db)):

    # check user tồn tại
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = models.Post(
        id=post.id,
        user_id=user_id,
        title=post.title,
        body=post.body
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    #Insert into posts (id, user_id, title, body) values (post.id, user_id, post.title, post.body)
    return db_post


@app.put("/users/{user_id}/posts/{post_id}")
def update_post(user_id: str, post_id: str, post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == user_id).first()
    # SELECT * FROM posts WHERE id = post_id AND user_id = user_id

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_post.title = post.title
    db_post.body = post.body

    db.commit()
    db.refresh(db_post)
    # UPDATE posts SET title = post.title, body = post.body WHERE id = post_id AND user_id = user_id
    return db_post


@app.delete("/users/{user_id}/posts/{post_id}")
def delete_post(user_id: str, post_id: str, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == user_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()
    # DELETE FROM posts WHERE id = post_id AND user_id = user_id
    return {"detail": "Post deleted successfully"}


# COMMENTS

@app.get("/posts/{post_id}/comments")
def get_comments(post_id: str, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    # SELECT * FROM comments WHERE post_id = post_id

    return comments


@app.post("/posts/{post_id}/comments")
def create_comment(post_id: str, comment: schemas.CommentCreate, db: Session = Depends(get_db)):

    # check post tồn tại
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # check user tồn tại
    user = db.query(models.User).filter(models.User.id == comment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_comment = models.Comment(
        id=comment.id,
        post_id=post_id,
        user_id=comment.user_id,
        text=comment.text
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    # Insert into comments (id, post_id, user_id, text) values (comment.id, post_id, comment.user_id, comment.text)
    return db_comment


@app.put("/posts/{post_id}/comments/{comment_id}")
def update_comment(post_id: str, comment_id: str, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.post_id == post_id).first()
    # SELECT * FROM comments WHERE id = comment_id AND post_id = post_id

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db_comment.text = comment.text

    db.commit()
    db.refresh(db_comment)
    # UPDATE comments SET text = comment.text WHERE id = comment_id AND post_id = post_id
    return db_comment


@app.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(post_id: str, comment_id: str, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.post_id == post_id).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()
    # DELETE FROM comments WHERE id = comment_id AND post_id = post_id
    return {"detail": "Comment deleted successfully"}