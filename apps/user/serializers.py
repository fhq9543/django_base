#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fanghuaqing'
__mtime__ = '2018/9/12'
"""
from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from user.functions import make_password
from user.models import UserInfo
from utils.serializer import BaseSerializer
from utils.string_extension import format_time


class UserCreateSerializer(BaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            instance = UserInfo()
            instance.role_id = validated_data.get("role_id", '')
            instance.username = validated_data.get("username", '')
            password = validated_data.get("password")
            instance.password = make_password(password)
            instance.save()
        return instance


class UserUpdateSerializer(BaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr in ["last_login", ]:
                value = format_time(datetime.now())
            setattr(instance, attr, value)
        with transaction.atomic():
            instance.save()
        return instance
