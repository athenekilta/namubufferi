from django.urls import path
from django.utils.text import slugify


def generic_path(model, views, name="detail", pk_url_kwarg="pk"):
    suffix = None
    if name == "list":
        suffix = ""
    elif name == "create":
        suffix = f"{name}/"
    elif name == "detail":
        suffix = f"<{pk_url_kwarg}>/"
    elif name in ("delete", "update"):
        suffix = f"<{pk_url_kwarg}>/{name}/"
    else:
        raise ValueError(name)

    return path(
        f"{slugify(model._meta.verbose_name_plural)}/{suffix}",
        eval(f"views.{model.__name__}{name.capitalize()}View.as_view()"),
        name=f"{slugify(model._meta.verbose_name)}-{name.lower()}",
    )


def generic_path_set(model, views, **kwargs):
    path_set = []
    for name in ("create", "delete", "detail", "list", "update"):
        try:
            path_set.append(generic_path(model=model, views=views, name=name, **kwargs))
        except AttributeError:
            continue
    return path_set
