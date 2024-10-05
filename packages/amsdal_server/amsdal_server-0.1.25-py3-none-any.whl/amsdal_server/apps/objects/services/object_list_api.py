from typing import Any

from amsdal_models.classes.constants import FILE_CLASS_NAME
from amsdal_models.classes.model import Model
from amsdal_models.querysets.executor import LAKEHOUSE_DB_ALIAS
from amsdal_utils.models.base import ModelBase
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.utils import Q
from starlette.authentication import BaseUser

from amsdal_server.apps.classes.mixins.column_info_mixin import ColumnInfoMixin
from amsdal_server.apps.classes.mixins.model_class_info import ModelClassMixin
from amsdal_server.apps.common.mixins.permissions_mixin import PermissionsMixin
from amsdal_server.apps.common.serializers.column_response import ColumnInfo
from amsdal_server.apps.common.serializers.fields_restriction import FieldsRestriction
from amsdal_server.apps.common.serializers.filter import Filter
from amsdal_server.apps.common.serializers.objects_response import ObjectsResponse
from amsdal_server.apps.common.utils import get_subclasses
from amsdal_server.apps.objects.mixins.object_data_mixin import ObjectDataMixin


class ObjectListApi(PermissionsMixin, ModelClassMixin, ColumnInfoMixin, ObjectDataMixin):
    @classmethod
    def fetch_objects(
        cls,
        user: BaseUser,
        base_url: str,
        class_name: str,
        *,
        filters: list[Filter] | None = None,
        include_metadata: bool = False,
        include_subclasses: bool = False,
        fields_restrictions: dict[str, FieldsRestriction] | None = None,
        load_references: bool = False,
        all_versions: bool = False,
        file_optimized: bool = False,
        page: int = 1,
        page_size: int | None = None,
        ordering: list[str] | None = None,
    ) -> ObjectsResponse:
        model_class = cls.get_model_class_by_name(class_name)
        permissions_info = cls.get_permissions_info(model_class, user)
        class_item: Model = cls.get_class_objects_qs().get(_address__object_id=class_name).execute()
        class_meta_item: Model = cls.get_class_object_metas_qs().get(_address__object_id=class_item.object_id).execute()

        class_properties: list[ColumnInfo] = cls.get_class_properties_by_class_and_meta(
            class_item,
            class_meta_item,
        )
        available_columns = [column.key for column in class_properties]
        available_columns += ['_metadata']
        fields_restriction = fields_restrictions.get(class_name) if fields_restrictions else None

        if fields_restriction:
            class_properties = [column for column in class_properties if column.key in fields_restriction.fields]
            fields_restriction.fields = [field for field in fields_restriction.fields if field in available_columns]

        if not permissions_info.has_read_permission:
            return ObjectsResponse(
                columns=class_properties,
                rows=[],
                total=0,
            )

        _filters = [
            _filter
            for _filter in (filters or [])
            if any(
                _filter.key == available_column or _filter.key.startswith(f'{available_column}__')
                for available_column in available_columns
            )
        ]

        rows, total = cls._fetch_objects(
            base_url,
            model_class,
            filters=_filters,
            fields_restrictions=fields_restrictions,
            include_metadata=include_metadata,
            include_subclasses=include_subclasses,
            load_references=load_references,
            all_versions=all_versions,
            file_optimized=file_optimized,
            page=page,
            page_size=page_size,
            ordering=ordering,
        )

        return ObjectsResponse(
            columns=class_properties,
            rows=rows,
            total=total,
        )

    @classmethod
    def _fetch_objects(
        cls,
        base_url: str,
        model_class: type[Model],
        filters: list[Filter],
        *,
        include_subclasses: bool = False,
        include_metadata: bool = False,
        fields_restrictions: dict[str, FieldsRestriction] | None = None,
        load_references: bool = False,
        all_versions: bool = False,
        file_optimized: bool = False,
        page: int = 1,
        page_size: int | None = None,
        ordering: list[str] | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        result: list[dict[str, Any]] = []
        total: int = 0
        classes: list[type[ModelBase]] = [model_class]

        if include_subclasses:
            for subclass in get_subclasses(model_class):
                classes.append(subclass)

        for _model_class in classes:
            if not issubclass(_model_class, Model):
                msg = 'Model class must be subclass of Model'
                raise TypeError(msg)

            qs = _model_class.objects.filter(
                _metadata__is_deleted=False,
                _address__object_version=Versions.ALL if all_versions else Versions.LATEST,
            )

            if all_versions:
                qs = qs.using(LAKEHOUSE_DB_ALIAS)

            if fields_restrictions:
                fields_restriction = fields_restrictions.get(_model_class.__name__, None)

                if fields_restriction:
                    qs = qs.only(fields_restriction.fields)

            is_optimized_file = model_class.__name__ == FILE_CLASS_NAME and file_optimized

            if is_optimized_file:
                qs = qs.only(['filename', 'size'])

            if filters:
                qs = qs.filter(
                    Q(**{f'{_filter.key}__{_filter.filter_type.name}': _filter.target for _filter in filters}),
                )

            total += qs.count().execute()

            if ordering is None:
                ordering = ['-_metadata__updated_at']

            qs = qs.order_by(*ordering)

            if page_size is not None:
                offset = (page - 1) * page_size
                limit = offset + page_size

                qs = qs[offset:limit]

            items: list[Model] = qs.execute()

            for item in items:
                result.append(
                    cls.build_object_data(
                        item,
                        base_url=base_url,
                        include_metadata=include_metadata,
                        fields_restrictions=fields_restrictions,
                        load_references=load_references,
                        is_file_object=is_optimized_file,
                    )
                )
        return result, total
