from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.predict, name='predict'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('board/', views.dashboard_view, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



 