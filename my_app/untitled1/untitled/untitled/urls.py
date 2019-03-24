"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from applp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'publisher_list/',views.publisher_list),
    # url(r'list/',views.publisher_list),
    url(r'add_shuju/',views.add_shuju),
    url(r'del_shuju/',views.del_shuju),
    url(r'edit_shuju/',views.edit_shuju),
    url(r'ziyemian/',views.ziyemian)
]
