#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fanghuaqing'
__mtime__ = '2018/12/13'
"""
import time

# serializer for JWT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature, BadData

from django_base.config import JWT_SECRET_KEY, JWT_ALG, JWT_SALT
from utils.log import logger


def genTokenSeq(user, expires):
    """
    token is generated as the JWT protocol.
    JSON Web Tokens(JWT) are an open, industry standard RFC 7519 method
    """
    s = Serializer(
        secret_key=JWT_SECRET_KEY,
        algorithm_name=JWT_ALG,
        salt=JWT_SALT,
        expires_in=expires
    )
    timestamp = time.time()
    return s.dumps(
        {
            'user_id': user.user_id,
            'role_id': user.role_id,
            'iat': timestamp
         }
    )


def tokenAuth(token):
    # token decoding
    s = Serializer(
        secret_key=JWT_SECRET_KEY,
        algorithm_name=JWT_ALG,
        salt=JWT_SALT
    )
    try:
        data = s.loads(token)
        # token decoding faild
        # if it happend a plenty of times, there might be someone
        # trying to attact your server, so it should be a warning.
    except SignatureExpired:
        # token已经超时失效
        msg = 'token expired'
        logger.warning(msg)
        return [None, None, msg]
    except BadSignature as e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                # token已经被篡改
                msg = 'token tampered'
                logger.warning(msg)
                return [None, None, msg]
        # payload不完整
        msg = 'badSignature of token'
        logger.warning(msg)
        return [None, None, msg]
    except:
        msg = 'wrong token with unknown reason'
        logger.warning(msg)
        return [None, None, msg]
    if ('user_id' not in data) or ('role_id' not in data):
        # 数据不合法，密钥和盐值泄露
        msg = 'illegal payload inside'
        logger.warning(msg)
        return [None, None, msg]
    msg = 'user(' + str(data['user_id']) + ') logged in by token.'
    # app.logger.info(msg)
    user_id = data['user_id']
    role_id = data['role_id']
    return [user_id, role_id, msg]
