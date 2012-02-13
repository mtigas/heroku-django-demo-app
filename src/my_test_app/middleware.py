from django.conf import settings
from django.http import HttpResponsePermanentRedirect, get_host

class ForceSSLMiddleware(object):
    """
    Redirects all (non-DEBUG) requests to go through SSL.

    Picks up the `HTTP_X_FORWARDED_PROTO` proxy header set by Heroku.

    Also sets the "Strict-Transport-Security" header for 600 seconds so that
    compliant browsers force all requests to this domain to use SSL.
    Can be disabled in settings:

        SSL_USE_STS_HEADER = False
    """
    def process_request(self, request):
        if not any([
            settings.DEBUG,
            request.is_secure(),
            request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'https'
        ]):
    	    return self._redirect(request)

    def process_response(self, request, response):
        return self._response_sts(response)

    def _redirect(self, request):
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError, \
        """Django can't perform a SSL redirect while maintaining POST data.
           Please structure your views so that redirects only occur during GETs."""

        url = request.build_absolute_uri(request.get_full_path())
        secure_url = url.replace("http://", "https://")
        return self._response_sts(HttpResponsePermanentRedirect(secure_url))

    def _response_sts(self, response):
        if not getattr(settings, "SSL_USE_STS_HEADER", True):
            return response

        response['Strict-Transport-Security'] = "max-age=600"
        return response

