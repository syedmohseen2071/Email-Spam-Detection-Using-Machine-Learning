"""spam email detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from spam_email_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('customerlogin', views.customer_login, name="customer_login"),
    path('customer_registration', views.customer_registration, name="customer_registration"),
    path('customer_home', views.customer_home, name="customer_home"),
    path('customer_profile', views.customer_profile, name="customer_profile"),
    path('customer_edit/<int:id>', views.customer_edit, name="customer_edit"),
    path('customer_update', views.customer_update, name="customer_update"),
    path('customer_delete/<int:id>', views.customer_delete, name="customer_delete"),
    path('customer_change_password', views.customer_change_password, name="customer_change_password"),
    path('customer_logout', views.customer_logout, name="customer_logout"),
    path('send_email', views.send_email, name="send_email"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('admin_change_password', views.admin_change_password, name="admin_change_password"),
    path('admin_logout', views.admin_logout, name="admin_logout"),
    path('view_customer', views.view_customer, name="view_customer"),
    path('admin_delete_customer/<int:id>', views.admin_delete_customer, name="admin_delete_customer"),
    path('inbox', views.inbox, name="inbox"),
    path('reply/<int:id>', views.reply, name="reply"),
    path('sent', views.sent, name="sent"),
    path('activate_request', views.activate_request, name="activate_request"),
    path('deactivate/<str:email>', views.deactivate, name="deactivate"),
    path('activate/<str:email>', views.activate, name="activate"),
    path('view_notification', views.view_notification, name="view_notification"),
    path('customer_view_notification', views.customer_view_notification, name="customer_view_notification"),
    path('add_notification', views.add_notification, name="add_notification"),
    path('delete_notification/<int:id>',views.delete_notification,name="delete_notification"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
