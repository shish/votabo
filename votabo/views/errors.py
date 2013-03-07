from pyramid.view import view_config

@view_config(renderer='errors/404.mako', context='pyramid.exceptions.NotFound')
def c404(request):
    request.response.status = "404 Not Found"
    return {}

@view_config(renderer='errors/403.mako', context='pyramid.exceptions.Forbidden')
def c403(request):
    request.response.status = "403 Permission Denied"
    return {}

