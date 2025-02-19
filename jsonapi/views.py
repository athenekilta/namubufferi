import re
from distutils.util import strtobool
from http import HTTPStatus

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.gzip import gzip_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .utils import make_jsonapi_document

MEDIA_TYPE = "application/vnd.api+json"  # https://jsonapi.org/


class JSONAPIResponse(JsonResponse):
    def __init__(self, data, content_type=MEDIA_TYPE, **kwargs):
        super().__init__(data, content_type=content_type, **kwargs)


class JSONAPIMixin:
    media_type = MEDIA_TYPE
    include = None
    fields_dict = None

    @method_decorator(vary_on_headers("Accept", "Cookie"))
    @method_decorator(gzip_page)
    def dispatch(self, request, *args, **kwargs):
        if request.content_type == self.media_type and request.content_params:
            return HttpResponse(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        errors = []
        for query_parameter in request.GET.keys():
            if re.match(r"page\[\w+\]$|filter\[\w+\]$", query_parameter):
                continue

            m = re.match(r"fields\[(\w+)\]$", query_parameter)
            if m:
                self.fields_dict = self.fields_dict or {}
                self.fields_dict[m.group(1)] = request.GET[query_parameter].split(",")
                continue

            if query_parameter == "paginate_by":
                self.paginate_by = int(request.GET[query_parameter])
                continue

            if query_parameter == "include":
                self.include = request.GET[query_parameter].split(",")
                continue

            if query_parameter.startswith("sort"):
                errors.append(
                    {
                        "source": {"parameter": query_parameter},
                        "title": "Not Implemented",
                    }
                )
            else:
                m = re.search(r"[A-Z0-9_-]", query_parameter)
                if not m:
                    errors.append(
                        {
                            "source": {
                                "parameter": query_parameter,
                            },
                            "links": {
                                "about": "https://jsonapi.org/format/#query-parameters"
                            },
                        }
                    )
        if errors:
            return JSONAPIResponse({"errors": errors}, status=HTTPStatus.BAD_REQUEST)

        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **kwargs):
        if self.request.GET.get("Accept") == self.media_type:
            return self.render_to_json_response(
                context, json_dumps_params={"indent": 2}, **kwargs
            )
        if self.request.headers.get("Accept") == self.media_type:
            return self.render_to_json_response(context, **kwargs)
        else:
            return super().render_to_response(context, **kwargs)

    def render_to_json_response(self, context, status=None, **kwargs):
        jsonapi_document = context["jsonapi_document"]
        return JSONAPIResponse(
            data=jsonapi_document,
            status=HTTPStatus.BAD_REQUEST if jsonapi_document.get("errors") else status,
            **kwargs,
        )

    def get_jsonapi_document(self, context):
        return make_jsonapi_document(
            objects=context.get("object_list") or context.get("object"),
            single="object_list" not in context.keys(),
            include=self.include,
            fields_dict=self.fields_dict,
            camel=strtobool(self.request.GET.get("camelCase", "1")),
        )

    def filter(self, queryset):
        query = self.request.GET.dict().copy()
        filter = {}
        for key in query.keys():
            m = re.match(r"filter\[(\w+)\]", key)
            if m:
                filter[m.group(1)] = query.get(key)
        return queryset.filter(**filter)

    def get_queryset(self):
        return self.filter(super().get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jsonapi_document"] = self.get_jsonapi_document(context)
        return context


class JSONAPIDeleteView(JSONAPIMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.headers.get("Accept") == self.media_type:
            return HttpResponse(status=HTTPStatus.NO_CONTENT)
        return response


class JSONAPIDetailView(JSONAPIMixin, DetailView):
    delete_view = None
    update_view = None

    def delete(self, request, *args, **kwargs):
        return self.delete_view.as_view()(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        return self.update_view.as_view()(request, *args, **kwargs)


class JSONAPICreateView(JSONAPIMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("Accept") == self.media_type:
            return self.render_to_json_response(
                self.get_context_data(),
                status=HTTPStatus.CREATED,
            )
        return response

    def form_invalid(self, form):
        if self.request.headers.get("Accept") == self.media_type:
            return JSONAPIResponse(
                {"errors": [{"meta": form.errors}]}, status=HTTPStatus.BAD_REQUEST
            )
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for key, value in self.request.GET.items():
            m = re.match(r"filter\[(\w+)\]", key)
            if m:
                field = form.fields[m.group(1)]
                values = value.split(",")
                field.queryset = field.queryset.filter(pk__in=values)
                field.empty_label = None
        return form


class JSONAPIListView(JSONAPIMixin, ListView):
    create_view = None
    page_kwarg = "page[number]"

    def post(self, request, *args, **kwargs):
        # https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/#an-alternative-better-solution
        return self.create_view.as_view()(request, *args, **kwargs)


class JSONAPIUpdateView(JSONAPIMixin, UpdateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("Accept") == self.media_type:
            return self.render_to_json_response(
                self.get_context_data(),
                status=HTTPStatus.OK,
            )
        return response

    def form_invalid(self, form):
        if self.request.headers.get("Accept") == self.media_type:
            return JSONAPIResponse(
                {"errors": [{"meta": form.errors}]}, status=HTTPStatus.BAD_REQUEST
            )
        return super().form_invalid(form)
