from django.db import models
from user.models import User as CustomUser
from account_book.models import BaseModel


class Book(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    amount = models.IntegerField(default=0)
    memo = models.TextField()

    class Meta:
        abstract = False
        managed = True
        db_table = "book"
