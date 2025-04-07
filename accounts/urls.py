from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('logout/',views.logout_page,name='logout')
]
