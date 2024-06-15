from django.urls import path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('lodging', views.LodgingViewSet, basename='lodging')
router.register('user', views.UserViewSet, basename='user')
router.register('owner', views.OwnerCreateViewSet, basename='owner')
# router.register('image_owner', views.ImageOwnerViewSet)
# router.register('image_lodging', views.ImageLodgingViewSet)
# router.register('service_price', views.SPriceViewSet)
router.register('post', views.PostViewSet)
router.register('follow', views.FollowViewSet, basename='follow')


urlpatterns = [
    #path('', views.index, name="index"),
    path('', include(router.urls)),
    # path('test/<int:x>/', views.test, name="test"),
    path('admin/', admin_site.urls),
]