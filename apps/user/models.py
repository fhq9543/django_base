from django.db import models


# Create your models here.
from django.db.models import ManyToManyField, DateTimeField

from utils.token import genTokenSeq


class UserInfo(models.Model):
    """用户"""
    user_id = models.AutoField(primary_key=True, verbose_name='用户ID')
    role_id = models.IntegerField(verbose_name='角色ID')
    username = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    last_login = models.DateTimeField(auto_now=True, verbose_name='最后一次登陆时间')

    class Meta:
        db_table = "user_info"

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)

            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, ManyToManyField):
                value = [ i.id for i in value ] if self.pk else None

            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

            data[f.name] = value
        return data

    def token(self, exprice):
        genTokenSeq(self, exprice)