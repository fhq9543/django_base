import base64
from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action

from user.functions import check_password, valid_serializer
from user.serializers import UserCreateSerializer, UserUpdateSerializer
from django_base.config import COOKIE_NAME
from utils.response import ResCode
from utils.string_extension import format_time
from utils.token import genTokenSeq, tokenAuth
from .models import UserInfo
from utils.http import APIResponse, APIResponseBadRequest


class UserRegisterAPIView(viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data, request=request)
        if not serializer.is_valid():
            error = valid_serializer(serializer)
            return APIResponse(success=False, msg=error)
        serializer.save()
        return APIResponse(msg="创建成功")


class ServerAPIView(viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserUpdateSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request):
        # 验证用户信息
        username = request.data['username']
        password = request.data['password']
        user_info = UserInfo.objects.filter(username=username).first()
        if not user_info:
            return APIResponse(success=False, msg="用户名或密码错误")
        encoded = user_info.password

        res = check_password(password, encoded)
        if not res:
            return APIResponse(success=False, msg="用户名或密码错误")

        # token
        access_token = genTokenSeq(user_info, 3600)

        # 更新登录时间
        user_info.last_login = format_time(datetime.now())
        user_info.save()

        response = APIResponse(msg="登陆成功")
        response["Authorization"] = access_token

        # 设置cookie
        response.set_cookie(COOKIE_NAME, access_token)
        return response

    @action(methods=["GET"], detail=False)
    def verify(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        if not access_token:
            return APIResponseBadRequest(msg="token not exist", success=False, rescode=ResCode.Token_Missing)
        res = tokenAuth(access_token)
        if not res[0]:
            return APIResponse(msg=res[2], success=False)
        return APIResponse(msg=res[2])
