from email.policy import default
from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from passlib.hash import bcrypt

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128)
    disabled = fields.BooleanField(default=False)
    #email = fields.CharField(max_length=100, default="fake_email")

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

##############################
from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []
##############################