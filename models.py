from sqlalchemy import Column, String, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from config import Base


#USER

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    # tạo B-tree index trên cột id để tăng tốc độ truy vấn theo id
    # CREATE INDEX idx_user_id ON users(id)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    # tạo B-tree index trên cột email để tăng tốc độ truy vấn theo email, unique=True để đảm bảo email không trùng lặp
    # CREATE INDEX idx_user_email ON users(email)
    age = Column(Integer)

    profile = relationship("Profile", back_populates="user", uselist=False)# quan hệ 1-1 với profile,1 user có 1 profile, uselist=False để chỉ định quan hệ 1-1
    posts = relationship("Post", back_populates="user")# quan hệ 1-n với post, 1 user có nhiều post


#PROFILE

class Profile(Base):
    __tablename__ = "profiles"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    # tạo B-tree index trên cột user_id để tăng tốc độ truy vấn theo user_id, đồng thời user_id cũng là khóa chính của bảng profiles
    # CREATE INDEX idx_profile_user_id ON profiles(user_id)
    address = Column(String)
    phone = Column(String)
    bio = Column(Text)

    user = relationship("User", back_populates="profile")# quan hệ 1-1 với user, 1 profile thuộc về 1 user


#POST

class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    # tạo B-tree index trên cột user_id để tăng tốc độ truy vấn theo user_id
    # CREATE INDEX idx_post_user_id ON posts(user_id)
    title = Column(String)
    body = Column(Text)

    user = relationship("User", back_populates="posts")# quan hệ 1-n với user, 1 post thuộc về 1 user
    comments = relationship("Comment", back_populates="post")# quan hệ 1-n với comment, 1 post có nhiều comment

    __table_args__ = (
        Index("idx_post_user", "user_id"),) # tạo B-tree index trên cột user_id để tăng tốc độ truy vấn theo user_id
#Create index idx_post_user on posts(user_id)

# COMMENT

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"), index=True)
    # tạo B-tree index trên cột post_id để tăng tốc độ truy vấn theo post_id
    # CREATE INDEX idx_comment_post ON comments(post_id)
    user_id = Column(String, ForeignKey("users.id"))
    # tạo B-tree index trên cột user_id để tăng tốc độ truy vấn theo user_id
    # CREATE INDEX idx_comment_user ON comments(user_id)
    text = Column(Text)

    post = relationship("Post", back_populates="comments")

    __table_args__ = (
        Index("idx_comment_post", "post_id"),
    )
# CREATE INDEX idx_comment_post ON comments(post_id)
