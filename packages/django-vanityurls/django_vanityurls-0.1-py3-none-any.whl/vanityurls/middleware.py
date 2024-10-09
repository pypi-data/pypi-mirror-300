from django.http.response import HttpResponsePermanentRedirect

from .models import VanityUrl


class VanityUrlsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # we only jump in if it's a 404
        if response.status_code != 404:
            return response

        req_path = request.path

        try:
            vurl = VanityUrl.objects.get(vanity_url=req_path)
            return HttpResponsePermanentRedirect(vurl.target)
        except:
            # return the original response unmolested
            return response
