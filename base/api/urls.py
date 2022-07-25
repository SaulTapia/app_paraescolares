from django.urls import path, re_path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MyTokenObtainPairView

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('students/', views.getStudents),
    re_path(r'^students/upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    path('wake/', views.wakeView),
]