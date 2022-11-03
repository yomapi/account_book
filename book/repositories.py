from account_book.repositories import BaseRepo
from book.models import Book
from book.serializers import BookSerializers


class BookRepo(BaseRepo):
    def find_with_limit(self, user_id: int, offset: int = 0, limit: int = 50):
        return self.serializer(
            self.model.objects.filter(user=user_id, deleted_at=None)[
                offset : limit + offset
            ],
            many=True,
        ).data

    def count(self, user_id: int):
        return self.model.objects.filter(user=user_id, deleted_at=None).count()


book_repo = BookRepo(model=Book, serializer=BookSerializers)
