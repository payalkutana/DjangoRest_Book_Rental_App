from django.urls import path
from authorization import views


# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('userapi',views.UserCreateView,basename='userapi')


urlpatterns = [
    path('signup',views.UserCreateView.as_view()),
]
