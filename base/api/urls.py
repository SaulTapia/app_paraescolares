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
    path('students/<str:matricula>/', views.GetStudent.as_view()),
    path('students/change/switchturn/', views.changeStudentTurn),

    path('wake/', views.wakeView),
    path('select/', views.selectView),
    path('select/change/', views.changeView),
    path('select/validate/', views.validateView),
    path('select/remove/', views.removeView),
    
    path('xlsx/group/', views.xlsxGroupView),
    path('xlsx/paraescolar/', views.xlsxParaescolarView),

    path('list/group/', views.getGroupList),
    path('list/paraescolar/', views.getParaescolarList),

    path('paraescolares/get/', views.getParaescolarView),
    path('paraescolares/getall/', views.getAllParaescolarView),
    path('paraescolares/make/', views.makeParaescolarView),
    path('paraescolares/change/', views.changeParaescolarView),
    path('paraescolares/delete/', views.deleteParaescolarView),

    path('teacher/register/', views.teacherRegister),
]