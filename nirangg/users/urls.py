from rest_framework import routers

from users.views import UsersViewSet
user_router = routers.DefaultRouter()


user_router.register(r'users', UsersViewSet)