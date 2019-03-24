from django.conf.urls import url
from my_crm.my_views import views

urlpatterns = [
    url(r'^customer_list/', views.CustomerList.as_view(), name='customer_list'),
    url(r'^my_customer/', views.CustomerList.as_view(), name='my_customer'),
    url(r'^user_list/', views.user_list),
    url(r'^customer_add/', views.customer_change, name='customer_add'),
    url(r'^customer_edit/(\d+)/', views.customer_change, name='customer_edit'),


]
