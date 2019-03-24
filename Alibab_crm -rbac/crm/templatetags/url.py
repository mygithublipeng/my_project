from django import template
from django.urls import reverse
from django.http import QueryDict

register = template.Library()


@register.simple_tag()
def reverse_url(request, name, *args, **kwargs):
    """
    反向解析生成URL，拼接参数
    :return:
    """
    # 根据传的url别名和参数反向解析生成基本的URL
    base_url = reverse(name, args=args, kwargs=kwargs)
    # 从当前的URL上获取参数 ——》  query=1&page=2
    params = request.GET.urlencode()
    # 如果没有条件 直接返回基本的URL
    if not params:
        return base_url
    # 返回带条件的URL
    return "{}?{}".format(base_url, params)


@register.simple_tag()
def rev_url(request, name, *args, **kwargs):
    """
    反向解析生成URL，拼接参数
    :return:
    """

    base_url = reverse(name, args=args, kwargs=kwargs)

    # 直接拿到当前的URL
    url = request.get_full_path()
    qd = QueryDict(mutable=True)
    qd['next'] = url
    return "{}?{}".format(base_url, qd.urlencode())
