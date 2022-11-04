from account_book.repositories import BaseRepo
from user.models import Token, User as CustomUser
from user.serializers import UserSerializers, TokenSerializers
from datetime import datetime


class UserRepo(BaseRepo):
    def get_by_email(self, email: str) -> dict:
        return self.serializer(
            self.model.objects.get(email=email, deleted_at=None)
        ).data


class TokenRepo(BaseRepo):
    def upsert(self, user_id: int, user: CustomUser, token: str):
        obj, created = self.model.objects.update_or_create(
            user=user_id,
            defaults={"user": user, "token": token, "deleted_at": None},
        )
        return self.serializer(obj).data

    def get_by_user_id(self, user: int) -> dict:
        try:
            return self.serializer(
                self.model.objects.get(user_id=user, deleted_at=None)
            ).data
        except self.model.DoesNotExist:
            return None

    def delete_by_user_id(self, user: int) -> None:
        token = self.model.objects.get(user_id=user, deleted_at=None)
        serilizer = self.serializer(
            token, data={"deleted_at": datetime.now()}, partial=True
        )

        self._validate_serializer_and_save(serilizer)


user_repo = UserRepo(model=CustomUser, serializer=UserSerializers)
token_repo = TokenRepo(model=Token, serializer=TokenSerializers)
