#!/usr/bin/env python
# -*- coding: utf-8 -*-

from account.models import Account
from django.contrib.auth.models import User

users = User.objects.all()
for user in users:
    try:
        Account.objects.get(user=user)
    except Account.DoesNotExist:
        Account(user=user).save()
