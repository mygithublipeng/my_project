from django.conf.urls import url
from crm.views import consultant
from crm.views import teacher

urlpatterns = [
    # 公户
    # url(r'^customer_list/', views.customer_list, name='customer_list'),
    url(r'^customer_list/', consultant.CustomerList.as_view(), name='customer_list'),
    # 私户
    # url(r'^my_customer/', views.customer_list, name='my_customer'),
    url(r'^my_customer/', consultant.CustomerList.as_view(), name='my_customer'),

    # url(r'^user_list/', consultant.user_list),

    # 添加客户
    # url(r'^customer_add/', views.customer_add, name='customer_add'),
    url(r'^customer_add/', consultant.customer_change, name='customer_add'),

    # 编辑客户
    # url(r'^customer_edit/(\d+)/', views.customer_edit, name='customer_edit'),
    url(r'^customer_edit/(\d+)/', consultant.customer_change, name='customer_edit'),

    # 展示跟进记录
    url(r'^consult_list/(0)/', consultant.ConsultList.as_view(), name='all_consult_list'),
    url(r'^consult_list/(?P<customer_id>\d+)/', consultant.ConsultList.as_view(), name='consult_list'),
    # 添加跟进记录
    url(r'^consult_add/', consultant.consult_add, name='consult_add'),

    # 编辑跟进记录
    url(r'^consult_edit/(\d+)/', consultant.consult_edit, name='consult_edit'),

    # 展示报名记录
    url(r'^enrollment_list/(?P<customer_id>\d+)/', consultant.EnrollmentList.as_view(), name='enrollment_list'),

    # 添加报名记录
    url(r'^enrollment_add/(?P<customer_id>\d+)/', consultant.enrollment, name='enrollment_add'),

    # 编辑报名记录
    url(r'^enrollment_edit/(?P<record_id>\d+)/', consultant.enrollment, name='enrollment_edit'),

    # 展示班级
    url(r'^class_list/', teacher.ClassList.as_view(), name='class_list'),

    # 添加班级
    url(r'^class_add/', teacher.classes, name='class_add'),

    # 编辑班级
    url(r'^class_edit/(\d+)/', teacher.classes, name='class_edit'),

    # 展示课程记录
    url(r'^course_record_list/(?P<class_id>\d+)', teacher.CourseRecordList.as_view(), name='course_record_list'),

    # 添加课程记录
    url(r'^course_record_add/(?P<class_id>\d+)', teacher.course_record, name='course_record_add'),

    # 编辑课程记录
    url(r'^course_record_edit/(?P<course_record_id>\d+)/', teacher.course_record, name='course_record_edit'),


    # 展示学习记录
    url(r'^study_record_list/(?P<course_record_id>\d+)/', teacher.study_record, name='study_record_list'),

]
