def wants_html(request):
    if getattr(request, 'htmx', False):
        return True
    return 'text/html' in request.META.get('HTTP_ACCEPT', '')

def htmx_redirect(url):
    from django.http import HttpResponse
    response = HttpResponse(status=200)
    response['HX-Redirect'] = url
    return response