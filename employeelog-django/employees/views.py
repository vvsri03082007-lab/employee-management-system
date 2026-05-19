from rest_framework.routers import DefaultRouter
from .views import EmployeeView

router = DefaultRouter()
router.register(r'employees', EmployeeView)

urlpatterns = router.urls