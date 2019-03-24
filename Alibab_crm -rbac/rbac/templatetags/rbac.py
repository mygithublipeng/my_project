from django import template
from django.conf import settings
import re
from collections import OrderedDict

register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_dict = request.session.get(settings.PERMISSION_MENU_KEY)

    url = request.path_info

    order_dict = OrderedDict()
    # for i in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
    #     order_dict[i] = menu_dict[i]
    #
    # for item in order_dict.values():
    #
    #     for i in item['children']:
    #         if re.match(r'^{}$'.format(i['url']), url):
    #             i['class'] = 'active'
    #             break

    #  [1,2]
    for i in sorted(menu_dict, key=lambda x: menu_dict[x]['weight'], reverse=True):
        # 复制到有序字典中
        order_dict[i] = menu_dict[i]
        # 取一级菜单的信息
        item = order_dict[i]

        item['class'] = 'hide'
        for i in item['children']:
            if i['id'] == request.current_parent_id:
                i['class'] = 'active'
                item['class'] = ''
                break

    return {'menu_list': order_dict.values()}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list = getattr(request, settings.BREADCRUMB)
    return {'breadcrumb_list': breadcrumb_list}


@register.filter()
def has_permission(request, name):
    # 判断name是否在权限的字典中
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params['rid'] = rid
    return params.urlencode()
