from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # CAPTCHA form page
    path('captcha_image/', views.captcha_image, name='captcha_image'),  # CAPTCHA image generation
    path('success/', views.success, name='success'),  # Success page after correct CAPTCHA
]
