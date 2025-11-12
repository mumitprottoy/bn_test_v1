from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import views, status, permissions, exceptions, parsers
from rest_framework_simplejwt.tokens import TokenError, RefreshToken

User = get_user_model()