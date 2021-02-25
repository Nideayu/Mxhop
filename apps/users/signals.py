from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()


# post_save:接收信号的方式
# sender:接收信号的model
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    # 是否创建，因为update的时候也会进行post_save
    if created:
        password = instance.password
        # instance相当于users
        instance.set_password(password)
        instance.save()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")
