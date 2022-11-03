from book.models import Book
from book.serializers import BookSerializers
from book.repositories import book_repo
from exceptions import NoPermissionError


class BookService:
    def __init__(self) -> None:
        self.model = Book
        self.serializer = BookSerializers

    def _validate_is_owner(self, book_data: dict, user_id: int):
        if book_data["user"] == user_id:
            return book_data
        else:
            raise NoPermissionError

    def get(self, book_id: int, user_id: int):
        return self._validate_is_owner(book_repo.get(book_id), user_id)

    def create(self, data: dict):
        return book_repo.create(data)

    def update(self, book_id: int, user_id: int, data: dict):
        self._validate_is_owner(book_repo.get(book_id), user_id)
        return book_repo.update(
            book_id,
            {
                **data,
                "id": book_id,
                "user_id": user_id,
            },
        )

    def delete(self, book_id: int, user_id: int):
        self._validate_is_owner(book_repo.get(book_id), user_id)
        book_repo.delete(book_id)
        return True

    def recover(self, book_id: int, user_id: int):
        self._validate_is_owner(book_repo.get(book_id, is_deleted=True), user_id)
        return book_repo.update(
            book_id, {"id": book_id, "deleted_at": None}, is_deleted=True
        )

    def find(self, user_id: int, offset: int = 0, limit: int = 50):
        return {
            "count": book_repo.count(user_id),
            "data": book_repo.find_with_limit(user_id, offset, limit),
        }


book_service = BookService()
