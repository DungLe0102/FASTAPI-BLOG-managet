from pydantic import BaseModel


#USER

class UserCreate(BaseModel):
    id: str
    name: str
    email: str
    age: int


class UserResponse(UserCreate):
    class Config:
        from_attributes = True


#PROFILE

class ProfileCreate(BaseModel):
    address: str
    phone: str
    bio: str


class ProfileResponse(ProfileCreate):
    user_id: str

    class Config:
        from_attributes = True


#POST

class PostCreate(BaseModel):
    id: str
    title: str
    body: str


class PostResponse(PostCreate):
    user_id: str

    class Config:
        from_attributes = True


# COMMENT 

class CommentCreate(BaseModel):
    id: str
    user_id: str
    text: str


class CommentResponse(CommentCreate):
    post_id: str

    class Config:
        from_attributes = True