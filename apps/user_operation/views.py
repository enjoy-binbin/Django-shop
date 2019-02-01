from django.shortcuts import render_to_response


def page_not_found(request, exception):
    """ 全局404处理函数 """
    response = render_to_response('base/404.html', {})
    response.code = 404
    return response


def page_error(request):
    """ 全局500处理函数 """
    res = render_to_response('base/500.html', {})
    res.status_code = 500
    return res
