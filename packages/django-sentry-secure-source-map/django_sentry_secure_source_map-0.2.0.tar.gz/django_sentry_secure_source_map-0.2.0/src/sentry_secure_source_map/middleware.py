from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseForbidden
from django.utils.crypto import constant_time_compare


class SentrySecureSourceMapMiddleware:
    """
    Only allow Sentry to access sourcemap files.
    """

    def __init__(self, get_response):
        self.sentry_security_token = getattr(settings, "SENTRY_SECURITY_TOKEN", "")

        if not self.sentry_security_token:
            raise MiddlewareNotUsed

        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(settings.STATIC_URL) and request.path.endswith(
            ".map"
        ):
            sentry_token = request.headers.get("X-Sentry-Token", "")

            if not constant_time_compare(sentry_token, self.sentry_security_token):
                return HttpResponseForbidden()

        return self.get_response(request)
