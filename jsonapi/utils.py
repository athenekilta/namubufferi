import json

from django.conf import settings
from django.core import serializers
from django.utils.text import slugify


def camelcase(s):
    return s[0].lower() + "".join(map(str.title, s.split("_")))[1:]


def camelcase_keys(d):
    d = d.copy()
    for key in list(d.keys()):
        if isinstance(d[key], dict):
            d[key] = camelcase_keys(d[key])
        if isinstance(d[key], list):
            d[key] = [camelcase_keys(i) for i in d[key]]
        d[camelcase(key)] = d.pop(key)
    return d


def snake_case(s):
    raise NotImplementedError()


def jsonapi_serialize(obj, fields):
    d = json.loads(
        serializers.serialize(
            "json",
            [obj],
            fields=None if fields == "__all__" else fields,
        )
    )[0]
    d.pop("model")
    d["type"] = slugify(obj._meta.verbose_name_plural)
    d["id"] = str(d.pop("pk"))
    d["attributes"] = d.pop("fields")

    # Relationships
    for field in obj._meta.get_fields():
        if field.is_relation and field.name in d["attributes"].keys():
            d["relationships"] = d.get("relationships") or {}
            if field.many_to_many:
                d["relationships"][
                    str(field.related_model._meta.verbose_name_plural)
                ] = {
                    "data": [
                        {
                            "type": field.related_model._meta.verbose_name_plural,
                            "id": str(pk),
                        }
                        for pk in d["attributes"].pop(field.name)
                    ]
                }

            else:
                d["relationships"][field.name] = {
                    "data": {
                        "type": field.related_model._meta.verbose_name_plural,
                        "id": str(d["attributes"].pop(field.name)),
                    }
                }

    # Property attributes
    for key, value in vars(type(obj)).items():
        if (
            isinstance(value, property)
            and (key in fields or fields == "__all__")
            and not key.startswith("_")
        ):
            d["attributes"][key] = getattr(obj, key)
    return d


def make_jsonapi_document(
    objects, include=None, single=False, camel=True, fields_dict=None
):
    data = []
    included = set()
    errors = []
    if objects is None:
        return {"data": None if single else [], "included": []}

    if single:
        objects = [objects]

    fields_dict = fields_dict or {}

    def get_fields(obj):
        if not hasattr(obj, "_meta"):
            raise NotImplementedError("RelatedManager include")
        verbose_name_plural = obj._meta.verbose_name_plural
        jsonapi_exposed_fields = settings.JSONAPI_EXPOSED_FIELDS.get(
            verbose_name_plural, "__all__"
        )
        fields = fields_dict.get(verbose_name_plural, jsonapi_exposed_fields)
        if jsonapi_exposed_fields == "__all__":
            return fields
        return set(fields).intersection(set(jsonapi_exposed_fields))

    for obj in objects:
        if obj is not None:
            data.append(jsonapi_serialize(obj, fields=get_fields(obj)))
            if include is not None:
                try:
                    included.update([getattr(obj, key) for key in include])
                except AttributeError as e:
                    errors.append(
                        {"source": {"parameter": "include"}, "detail": str(e)}
                    )
                    break
    included = [
        jsonapi_serialize(obj, fields=get_fields(obj))
        for obj in included
        if obj is not None
    ]
    if single:
        data = data[0]

    jsonapi_document = {}
    if errors:
        jsonapi_document["errors"] = errors
    else:
        jsonapi_document["data"] = data
        if include:
            jsonapi_document["included"] = included
    if camel:
        jsonapi_document = camelcase_keys(jsonapi_document)
    return jsonapi_document
