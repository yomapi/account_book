from account_book.models import BaseModel
from account_book.serializers import BaseSerializers
from datetime import datetime


class BaseRepo:
    def __init__(self, model: BaseModel, serializer: BaseSerializers):
        self.model = model
        self.serializer = serializer

    def _validate_serializer_and_save(self, serializer: BaseSerializers) -> dict:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get(self, data_id: int) -> dict:
        return self.serializer(self.model.objects.get(id=data_id, deleted_at=None)).data

    def create(self, data: dict) -> dict:
        serializer = self.serializer(data=data)
        return self._validate_serializer_and_save(serializer)

    def update(self, data: dict) -> dict:
        serializer = self.serializer(data=data, partial=True)
        return self._validate_serializer_and_save(serializer)

    def delete(self, data_id: int, soft_delete: bool = True) -> None:
        if soft_delete:
            self.update({"id": data_id, "deleted_at": datetime.now()})
        else:
            self.model.objects.get(id=data_id).delete()
        return
