from django import forms
from my_crm import models
from django.core.exceptions import ValidationError
import hashlib


class BootstrapForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RegForm(BootstrapForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='密码', min_length=6)
    re_password = forms.CharField(widget=forms.PasswordInput(), label='确认密码', min_length=6)

    class Meta:
        model = models.UserProfile
        fields = "__all__"
        exclude = ['is_active']

        labels = {
            'username': '用户名',
            'password': '密码',
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
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            pwd = md5.hexdigest()
            print(pwd)
            self.cleaned_data['password'] = pwd
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')

class CustomerForm(BootstrapForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs = {}
