# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Authentication:
    def __init__(self):
        pass


class AuthSession(Authentication):
    def __init__(self):
        pass


class AuthToken(Authentication):
    def __init__(self):
        pass


class AuthOauth(Authentication):
    def __init__(self):
        pass


class AuthCustom(Authentication):
    def __init__(self):
        pass

    def validate(self):
        return True


class Authorization:
    def __init__(self):
        pass

    def is_authorized(self):
        return True