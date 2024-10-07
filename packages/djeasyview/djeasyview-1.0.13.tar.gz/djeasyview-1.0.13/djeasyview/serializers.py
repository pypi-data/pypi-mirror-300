from rest_framework import serializers
from django.core.exceptions import ValidationError
from typing import Any


class DjeasyModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = "__all__"

    @classmethod
    def options(
        cls,
        model_name,
        queryset=None,
        fields="__all__",
        many=True,
        related_fields=None,
        *args,
        **kwargs,
    ):
        return cls(
            model=model_name,
            fields=fields,
            instance=queryset,
            many=many,
            related_fields=related_fields,
            *args,
            **kwargs,
        )

    def __init__(
        self,
        model=None,
        fields="__all__",
        related_fields=None,
        *args: Any,
        **kwargs: Any,
    ):
        self.display_fields = kwargs.pop("display_fields", None)
        self.access_fields = kwargs.pop("access_fields", None)
        self.rename_fields = kwargs.pop("rename_fields", None)

        if model and self.Meta.model is None:
            self.Meta.model = model
            self.Meta.fields = fields

        super(DjeasyModelSerializer, self).__init__(*args, **kwargs)
        self.get_display_fields()
        self.get_access_fields()
        self.get_renaming_fields()

        if related_fields:
            for related_field, related_field_options in related_fields.items():
                self.fields[related_field] = self.serializer_related_to_field(
                    **related_field_options
                )

    def get_display_fields(self):
        if self.display_fields is not None:
            allowed = set(self.display_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_access_fields(self):
        if self.access_fields:
            for field_name, access_type in self.access_fields.items():
                if access_type not in ["read_only", "write_only"]:
                    raise ValidationError(
                        "The type should be either 'read_only' or 'write_only'"
                    )
                if access_type == "read_only" and field_name in self.fields:
                    self.fields[field_name].read_only = True
                elif access_type == "write_only" and field_name in self.fields:
                    self.fields[field_name].write_only = True

    def get_renaming_fields(self):
        if self.rename_fields:
            for old_name, new_name in self.rename_fields.items():
                if old_name in self.fields:
                    self.fields[new_name] = self.fields.pop(old_name)
