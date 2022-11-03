from django.db import models
from account_book.models import BaseModel


class User(BaseModel):
    email = models.CharField(max_length=50, unique=True, null=False, default="")
    password = models.CharField(max_length=255, null=False, default="")

    class Meta:
        abstract = False
        managed = True
        db_table = "user"


class Token(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    token = models.CharField(max_length=255, default=None)

    class Meta:
        abstract = False
        managed = True
        db_table = "user_token"
