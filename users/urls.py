from .apps import UsersConfig
from .views import PaymentViewSet
from rest_framework.routers import DefaultRouter

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"payment", PaymentViewSet, basename="payment")

urlpatterns = []
urlpatterns += router.urls
