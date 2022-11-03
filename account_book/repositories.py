from account_book.models import BaseModel
from account_book.serializers import BaseSerializers
from datetime import datetime


class BaseRepo:
    def __init__(self, model: BaseModel, serializer: BaseSerializers):
        self.model = model
        self.serializer = serializer

    def _get_query_by_soft_deleted(self, data_id: int, is_deleted: bool):
        return (
            self.model.objects.get(id=data_id)
            if is_deleted
            else self.model.objects.get(id=data_id, deleted_at=None)
        )

    def _validate_serializer_and_save(self, serializer: BaseSerializers) -> dict:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get(self, data_id: int, is_deleted: bool = False) -> dict:
        query = self._get_query_by_soft_deleted(data_id, is_deleted)
        return self.serializer(query).data

    def create(self, data: dict) -> dict:
        serializer = self.serializer(data=data)
        return self._validate_serializer_and_save(serializer)

    def update(self, data_id: int, data: dict, is_deleted: bool = False) -> dict:
        target = self._get_query_by_soft_deleted(data_id, is_deleted)
        serializer = self.serializer(target, data=data, partial=True)
        return self._validate_serializer_and_save(serializer)

    def delete(self, data_id: int, soft_delete: bool = True) -> None:
        if soft_delete:
            self.update(data_id, {"id": data_id, "deleted_at": datetime.now()})
        else:
            self.model.objects.get(id=data_id).delete()
        return
