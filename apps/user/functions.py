#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fanghuaqing'
__mtime__ = '2018/12/13'
"""
import base64
import hashlib
from utils.secret import default_gen_secret_key


def make_password(password):
    pwd = bytes(password, encoding="utf-8")
    salt = bytes(default_gen_secret_key(12), encoding="utf-8")
    iterations = 100000
    digest = "sha256"       # digest  算法，使用 sha256

    x = hashlib.pbkdf2_hmac(digest, pwd, salt, iterations, 32)
    code = base64.b64encode(x)

    encoded = "pbkdf2_sha256" + "$" + str(iterations) + "$" + str(salt, encoding="utf8") + "$" + str(code, encoding="utf8")
    return encoded


def check_password(password, encoded):
    encodeds = encoded.split("$")
    pwd = bytes(password, encoding="utf-8") # 用户设置的原始密码
    salt = bytes(encodeds[2], encoding="utf-8") # 盐
    iterations = encodeds[1] # 加密算法的迭代次数
    digest = "sha256"       # digest  算法，使用 sha256

    # 第一步：使用  pbkdf2 算法加密
    x = hashlib.pbkdf2_hmac(digest, pwd, salt, int(iterations), 32)

    # 第二步：Base64  编码
    code = base64.b64encode(x)

    # 第三步：组合加密算法、迭代次数、盐、密码和分割符号 "$"
    encoded2 = "pbkdf2_sha256" + "$" + iterations + "$" + str(salt, encoding="utf8") + "$" + str(code, encoding="utf8")
    return encoded == encoded2


def valid_serializer(serializer):
    errors = [key + ':' + value[0] for key, value in serializer.errors.items() if isinstance(value, list)]
    error = ""
    if errors:
        error = errors[0]
        error = error.lstrip(':')
    else:
        for key, value in serializer.errors.items():
            if isinstance(value, dict):
                key, value = value.popitem()
                error = key + ':' + value[0]
                break
    return error
