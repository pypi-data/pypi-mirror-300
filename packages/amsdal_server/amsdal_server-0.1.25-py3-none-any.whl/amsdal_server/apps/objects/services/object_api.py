import base64
from typing import Any

from amsdal_data.transactions.decorators import transaction
from amsdal_models.classes.errors import AmsdalUniquenessError
from amsdal_models.classes.errors import ObjectAlreadyExistsError
from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.model import Model
from amsdal_models.querysets.errors import ObjectDoesNotExistError
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import SchemaTypes
from pydantic import BaseModel
from starlette.authentication import BaseUser

from amsdal_server.apps.classes.errors import ClassNotFoundError
from amsdal_server.apps.common.errors import AmsdalPermissionError
from amsdal_server.apps.common.mixins.permissions_mixin import PermissionsMixin
from amsdal_server.apps.common.permissions.enums import AccessTypes
from amsdal_server.apps.objects.mixins.object_data_mixin import ObjectDataMixin


class BulkAddressBody(BaseModel):
    address: str


class BulkUpdateBody(BulkAddressBody):
    data: dict[str, Any]


class ObjectApi(PermissionsMixin, ObjectDataMixin):
    @classmethod
    def create_object(
        cls,
        user: BaseUser,
        base_url: str,
        class_name: str,
        data: dict[str, Any],
        *,
        load_references: bool = False,
    ) -> dict[str, Any]:
        model_class = cls._get_model_class_and_check_permissions(
            user,
            class_name=class_name,
            access_type=AccessTypes.CREATE,
        )
        _data = cls._decode_bytes(data)
        object_item = model_class(**_data)

        try:
            object_item.save(
                force_insert='_object_id' in data,
            )
        except ObjectAlreadyExistsError as e:
            msg = 'Object with the same ID already exists'
            raise ValueError(msg) from e

        except AmsdalUniquenessError as e:
            raise ValueError(str(e)) from e

        return cls.build_object_data(
            object_item,
            base_url=base_url,
            load_references=load_references,
            include_metadata=True,
        )

    @classmethod
    def bulk_create_objects(
        cls,
        user: BaseUser,
        base_url: str,
        class_name: str,
        data: list[dict[str, Any]],
        *,
        load_references: bool = False,
    ) -> list[dict[str, Any]]:
        model_class = cls._get_model_class_and_check_permissions(
            user,
            class_name=class_name,
            access_type=AccessTypes.CREATE,
        )
        _data = cls._decode_bytes(data)

        object_items = []
        for object_data in _data:
            if '_object_id' in object_data:
                msg = 'Object ID cannot be provided for bulk create'
                raise ValueError(msg)

            object_items.append(model_class(**object_data))

        try:
            model_class.objects.bulk_create(object_items)
        except ObjectAlreadyExistsError as e:
            msg = 'Object with the same ID already exists'
            raise ValueError(msg) from e

        except AmsdalUniquenessError as e:
            raise ValueError(str(e)) from e

        return [
            cls.build_object_data(
                object_item,
                base_url=base_url,
                load_references=load_references,
                include_metadata=True,
            )
            for object_item in object_items
        ]

    @classmethod
    def validate_object(
        cls,
        class_name: str,
        data: dict[str, Any],
    ) -> None:
        model_class = cls._get_model_class(class_name=class_name)
        model_class(**data)

    @classmethod
    def update_object(
        cls,
        user: BaseUser,
        base_url: str,
        address: str,
        data: dict[str, Any],
        *,
        load_references: bool = False,
    ) -> dict[str, Any]:
        _address = Address.from_string(address)
        model_class = cls._get_model_class_and_check_permissions(
            user,
            class_name=_address.class_name,
            access_type=AccessTypes.UPDATE,
        )

        object_item = model_class.objects.get(
            _metadata__is_deleted=False,
            _address__object_id=_address.object_id,
            _address__class_version=_address.class_version,
            _address__object_version=_address.object_version,
        ).execute()

        cls._check_object_permissions(object_item, user, AccessTypes.UPDATE)

        _data = cls._decode_bytes(data)
        updated_item = model_class(
            **_data,
            _metadata=object_item.get_metadata(),
            _object_id=object_item.object_id,
            _object_version=object_item.object_version,
        )

        try:
            updated_item.save()
        except AmsdalUniquenessError as e:
            raise ValueError(str(e)) from e

        return cls.build_object_data(updated_item, base_url=base_url, load_references=load_references)

    @classmethod
    @transaction
    def bulk_update_objects(
        cls,
        user: BaseUser,
        base_url: str,
        data: list[BulkUpdateBody],
        *,
        load_references: bool = False,
    ) -> list[dict[str, Any]]:
        objects_to_update: dict[str, list[Model]] = {}

        for data_item in data:
            _address = Address.from_string(data_item.address)
            model_class = cls._get_model_class_and_check_permissions(
                user,
                class_name=_address.class_name,
                access_type=AccessTypes.UPDATE,
            )
            objects_to_update.setdefault(_address.class_name, [])

            object_item = model_class.objects.get(
                _metadata__is_deleted=False,
                _address__object_id=_address.object_id,
                _address__class_version=_address.class_version,
                _address__object_version=_address.object_version,
            ).execute()

            cls._check_object_permissions(object_item, user, AccessTypes.UPDATE)

            _data = cls._decode_bytes(data_item.data)
            objects_to_update[_address.class_name].append(
                model_class(
                    **_data,
                    _metadata=object_item.get_metadata(),
                    _object_id=object_item.object_id,
                    _object_version=object_item.object_version,
                )
            )

        result_objects = []
        for class_name, objects in objects_to_update.items():
            model_class = cls._get_model_class_and_check_permissions(
                user,
                class_name=class_name,
                access_type=AccessTypes.UPDATE,
            )
            model_class.objects.bulk_update(objects)
            result_objects.extend(objects)

        return [
            cls.build_object_data(updated_item, base_url=base_url, load_references=load_references)
            for updated_item in result_objects
        ]

    @classmethod
    def partial_update_object(
        cls,
        user: BaseUser,
        base_url: str,
        address: str,
        data: dict[str, Any],
        *,
        load_references: bool = False,
    ) -> dict[str, Any]:
        _address = Address.from_string(address)
        model_class = cls._get_model_class_and_check_permissions(
            user,
            class_name=_address.class_name,
            access_type=AccessTypes.UPDATE,
        )

        object_item = model_class.objects.get(
            _metadata__is_deleted=False,
            _address__object_id=_address.object_id,
            _address__class_version=_address.class_version,
            _address__object_version=_address.object_version,
        ).execute()
        cls._check_object_permissions(object_item, user, AccessTypes.UPDATE)

        _data = cls._decode_bytes(data)

        for _field, _value in _data.items():
            if hasattr(object_item, _field):
                setattr(object_item, _field, _value)

        try:
            object_item.save()
        except AmsdalUniquenessError as e:
            raise ValueError(str(e)) from e

        return cls.build_object_data(object_item, base_url=base_url, load_references=load_references)

    @classmethod
    @transaction
    def bulk_partial_update_objects(
        cls,
        user: BaseUser,
        base_url: str,
        data: list[BulkUpdateBody],
        *,
        load_references: bool = False,
    ) -> list[dict[str, Any]]:
        objects_to_update: dict[str, list[Model]] = {}

        for data_item in data:
            _address = Address.from_string(data_item.address)
            model_class = cls._get_model_class_and_check_permissions(
                user,
                class_name=_address.class_name,
                access_type=AccessTypes.UPDATE,
            )
            objects_to_update.setdefault(_address.class_name, [])

            object_item = model_class.objects.get(
                _metadata__is_deleted=False,
                _address__object_id=_address.object_id,
                _address__class_version=_address.class_version,
                _address__object_version=_address.object_version,
            ).execute()
            cls._check_object_permissions(object_item, user, AccessTypes.UPDATE)

            _data = cls._decode_bytes(data_item.data)

            for _field, _value in _data.items():
                if hasattr(object_item, _field):
                    setattr(object_item, _field, _value)

            objects_to_update[_address.class_name].append(object_item)

        result_objects = []
        for class_name, objects in objects_to_update.items():
            model_class = cls._get_model_class_and_check_permissions(
                user,
                class_name=class_name,
                access_type=AccessTypes.UPDATE,
            )
            model_class.objects.bulk_update(objects)
            result_objects.extend(objects)

        return [
            cls.build_object_data(updated_item, base_url=base_url, load_references=load_references)
            for updated_item in result_objects
        ]

    @classmethod
    def delete_object(
        cls,
        user: BaseUser,
        address: str,
    ) -> None:
        _address = Address.from_string(address)
        model_class = cls._get_model_class_and_check_permissions(
            user,
            class_name=_address.class_name,
            access_type=AccessTypes.DELETE,
        )
        object_item = model_class.objects.get(
            _metadata__is_deleted=False,
            _address__object_id=_address.object_id,
            _address__class_version=_address.class_version,
            _address__object_version=_address.object_version,
        ).execute()
        cls._check_object_permissions(object_item, user, AccessTypes.DELETE)
        object_item.delete()

    @classmethod
    @transaction
    def bulk_delete_objects(cls, user: BaseUser, data: list[BulkAddressBody]) -> None:
        objects_to_delete: dict[str, list[Model]] = {}

        for data_item in data:
            _address = Address.from_string(data_item.address)
            model_class = cls._get_model_class_and_check_permissions(
                user,
                class_name=_address.class_name,
                access_type=AccessTypes.DELETE,
            )
            objects_to_delete.setdefault(_address.class_name, [])

            object_item = model_class.objects.get(
                _metadata__is_deleted=False,
                _address__object_id=_address.object_id,
                _address__class_version=_address.class_version,
                _address__object_version=_address.object_version,
            ).execute()
            cls._check_object_permissions(object_item, user, AccessTypes.DELETE)
            objects_to_delete[_address.class_name].append(object_item)

        for class_name, objects in objects_to_delete.items():
            model_class = cls._get_model_class_and_check_permissions(
                user,
                class_name=class_name,
                access_type=AccessTypes.UPDATE,
            )
            model_class.objects.bulk_delete(objects)

    @classmethod
    def _get_model_class_and_check_permissions(
        cls,
        user: BaseUser,
        class_name: str,
        access_type: AccessTypes,
    ) -> type[Model]:
        model_class = cls._get_model_class(class_name)
        permissions_info = cls.get_permissions_info(
            model_class,
            user,
            access_types=[access_type],
        )
        has_access = getattr(permissions_info, f'has_{access_type.value}_permission')

        if not has_access:
            raise AmsdalPermissionError(
                access_type=access_type,
                class_name=class_name,
            )
        return model_class

    @classmethod
    def _check_object_permissions(
        cls,
        obj: Model,
        user: BaseUser,
        access_type: AccessTypes,
    ) -> Model:
        if obj:
            permissions_info = cls.get_permissions_info(obj.__class__, user, obj=obj)
            has_access = getattr(permissions_info, f'has_{access_type.value}_permission')

            if not has_access:
                raise AmsdalPermissionError(
                    access_type=access_type,
                    class_name=obj.__class__.__name__,
                )

        return obj

    @classmethod
    def _get_model_class(
        cls,
        class_name: str,
    ) -> type[Model]:
        class_manager = ClassManager()
        class_object: type[Model] = class_manager.import_model_class('ClassObject', SchemaTypes.CORE)

        try:
            class_item = class_object.objects.latest().get(_address__object_id=class_name).execute()
        except ObjectDoesNotExistError as e:
            raise ClassNotFoundError(class_name) from e

        return class_manager.import_model_class(
            class_item.object_id,  # type: ignore[arg-type]
            class_item.get_metadata().class_schema_type,
        )

    @classmethod
    def _decode_bytes(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {key: cls._decode_bytes(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [cls._decode_bytes(item) for item in data]
        elif isinstance(data, str) and data.startswith('data:binary;base64, '):
            return base64.b64decode(data.replace('data:binary;base64, ', '').encode('utf-8'))
        return data
