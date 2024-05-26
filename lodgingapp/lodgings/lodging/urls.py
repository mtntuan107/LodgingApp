from django.urls import path
from . import views
from .admin import admin_site


urlpatterns = [
    path('', views.index, name="index"),
    path('test/<int:x>/', views.test, name="test"),
    path('admin/', admin_site.urls),

]