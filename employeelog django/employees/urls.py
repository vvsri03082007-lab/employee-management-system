from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeView, DeletedEmployeeView

router = DefaultRouter()

router.register('employees', EmployeeView, basename='employees')

router.register('deleted-employees', DeletedEmployeeView, basename='deleted-employees')

urlpatterns = [

    path('', include(router.urls)),

]
