from django import forms
from crm import models
from django.core.exceptions import ValidationError
import hashlib


class BootstrapForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# 注册form
class RegForm(BootstrapForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='密码', min_length=6)
    re_password = forms.CharField(widget=forms.PasswordInput(), label='确认密码', min_length=6)

    class Meta:
        model = models.UserProfile
        fields = "__all__"  # 所有字段
        # fields = ['username','password']
        exclude = ['is_active']  # 排除某些字段

        labels = {
            'username': '用户名',
            'password': '密码',
            # 're_password': '确认密码',
            'department': '部门',
        }

        widgets = {
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

        error_messages = {
            'username': {
                'required': '不能为空',
                'invalid': '格式错误'
            }
        }

    def clean(self):
        pwd = self.cleaned_data.get('password', '')
        re_pwd = self.cleaned_data.get('re_password', )
        if pwd == re_pwd:
            # 对密码进行加密
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            pwd = md5.hexdigest()
            print(pwd)
            self.cleaned_data['password'] = pwd
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


# 客户Form
class CustomerForm(BootstrapForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 执行父类的__init__
        self.fields['course'].widget.attrs.pop('class')


# 跟进记录Form
class ConsultForm(BootstrapForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete_status'].widget.attrs.pop('class')
        # 当前登录的用户（销售）
        print(self.instance.consultant)
        # self.fields['customer'].choices = [('', '---------'), (2, '239966930011'),]

        customer_choices = [(i.pk, str(i)) for i in self.instance.consultant.customers.all()]
        customer_choices.insert(0, ('', '---------'))

        self.fields['customer'].choices = customer_choices
        # print(list(self.fields['customer'].widget.choices))
        self.fields['consultant'].choices = [(self.instance.consultant.pk, self.instance.consultant.name)]


# 报名记录Form
class EnrollmentForm(BootstrapForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.customer_id != '0':
            # 限制客户是当前的客户
            self.fields['customer'].choices = [(self.instance.customer_id, str(self.instance.customer))]
            # 限制客户可选的班级是记录中已报的班级
            self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]


# 班级Form
class ClassForm(BootstrapForm):
    class Meta:
        model = models.ClassList
        fields = "__all__"


# 课程记录Form
class CourseRecordForm(BootstrapForm):
    class Meta:
        model = models.CourseRecord
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 限制班级是当前的班级
        self.fields['re_class'].choices = [(self.instance.re_class_id, str(self.instance.re_class))]
        # 限制老师是当前的班主任
        self.fields['teacher'].choices = [(self.instance.teacher_id, str(self.instance.teacher))]


# 学习记录Form
class StudyRecordForm(BootstrapForm):
    class Meta:
        model = models.StudyRecord
        fields = "__all__"
