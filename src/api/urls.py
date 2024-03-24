from rest_framework.routers import DefaultRouter

from api.views import CargoViewSet, LocationViewSet, TruckViewSet

router = DefaultRouter()
router.register(r'cargo', CargoViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'trucks', TruckViewSet)

urlpatterns = router.urls
