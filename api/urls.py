
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'v1/claims', views.ClaimViewSet)
router.register(r'v1/organizations', views.OrganizationViewSet)
router.register(r'v1/claim_types', views.ClaimTypeViewSet)
