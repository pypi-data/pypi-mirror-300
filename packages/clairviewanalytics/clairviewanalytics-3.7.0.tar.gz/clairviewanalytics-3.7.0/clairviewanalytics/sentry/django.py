from django.conf import settings
from sentry_sdk import configure_scope

from clairviewanalytics.sentry import CLAIRVIEW_ID_TAG

GET_DISTINCT_ID = getattr(settings, "CLAIRVIEW_DJANGO", {}).get("distinct_id")


def get_distinct_id(request):
    if not GET_DISTINCT_ID:
        return None
    try:
        return GET_DISTINCT_ID(request)
    except:  # noqa: E722
        return None


class ClairviewDistinctIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with configure_scope() as scope:
            distinct_id = get_distinct_id(request)
            if distinct_id:
                scope.set_tag(CLAIRVIEW_ID_TAG, distinct_id)
            response = self.get_response(request)
        return response
