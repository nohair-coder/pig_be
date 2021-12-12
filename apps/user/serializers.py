from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户
    """

    class Meta:
        model = User
        fields = ("username", "password", "email")


class UserRegSerializer(serializers.ModelSerializer):
    # write_only=True设置不被序列化
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    # print(username)
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validate(self, attrs):
        attrs["email"] = attrs["username"]+'@qq.com'
        return attrs

    class Meta:
        model = User
        fields = ("username",  "email", "password")
