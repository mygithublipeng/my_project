from django.db import models

# Create your models here.
class Publisher(models.Model):
    pid = models.AutoField(primary_key=True) #pid 主键
    name = models.CharField(max_length=32,unique=True) #出版设名称
    def __str__(self):
        return self.name


