from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EmployeeView, DeletedEmployeeView, CompanyView, DynamicFieldView, 
    onboard_company, verify_onboard, request_otp, verify_otp, MyTokenObtainPairView,
    CoworkerListViewSet, ConversationViewSet, MessageViewSet, AnnouncementViewSet, 
    NotificationViewSet, presence_heartbeat, user_profile
)

router = DefaultRouter()
router.register(r'companies', CompanyView)
router.register(r'employees', EmployeeView, basename='employee')
router.register(r'deleted-employees', DeletedEmployeeView, basename='deleted-employee')
router.register(r'dynamic-fields', DynamicFieldView, basename='dynamic-field')
router.register(r'coworkers', CoworkerListViewSet, basename='coworker')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
    path('conversations/<int:conversation_id>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('messages/<int:pk>/', MessageViewSet.as_view({'delete': 'destroy'})),
    path('presence/heartbeat/', presence_heartbeat),
    path('profile/', user_profile),
    path('onboard/', onboard_company),
    path('verify-onboard/', verify_onboard),
    path('request-otp/', request_otp),
    path('verify-otp/', verify_otp),
    path('token/', MyTokenObtainPairView.as_view()),
]