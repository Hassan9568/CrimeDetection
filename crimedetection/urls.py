"""
URL configuration for crimedetection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps import views
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),   
    path('home/',views.HomePage,name='home'),
    path('detect_anomaly/',views.DetectAnomaly,name='detect_anomaly'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('clear-data/', views.clear_data, name='clear_data'),
    path('screenshot_list/', views.screenshot_list, name='screenshot_list'),
    path('admin/', admin.site.urls), 
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ... the rest of your URLconf goes here ...

# if settings.DEBUG:
#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]