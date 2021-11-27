"""issue_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url
from .api import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('issue/<int:pk>', GetIssueDetails.as_view(),
        name='get_issue_details'),
    url(r'^issue/list', GetIssueLists.as_view(), name='get_issue_list'),
    url(r'^issue/create', CreateIssue.as_view(), name='create_issue'),
    path('issue/<str:search_name>',FilterIssue.as_view(),name="filter_issue"),
    path('bot/<str:message>',GetBotResponse.as_view(),name="get_bot_response"),
]
