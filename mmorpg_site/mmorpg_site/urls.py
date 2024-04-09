"""
URL configuration for mmorpg_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from board.views import index, about, advertisement_list, create_advertisement, advertisement_detail, create_response, private_responses, edit_advertisement
from users.views import confirm_email, register, activate, user_login, user_logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about', about, name='about'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('advertisements/', advertisement_list, name='advertisement_list'),
    path('advertisements/<str:category>/', advertisement_list, name='advertisement_list_by_category'),
    path('create_advertisement/', create_advertisement, name='create_advertisement'),
    path('advertisement/<int:pk>/', advertisement_detail, name='advertisement_detail'),
    path('create_response/<int:advertisement_id>/', create_response, name='create_response'),
    path('private-responses/', private_responses, name='private_responses'),
    path('advertisement/edit/<int:pk>/', edit_advertisement, name='advertisement_edit'),
]
